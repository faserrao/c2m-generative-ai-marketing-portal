"""CDSGenAI API constructs."""

import os

import aws_cdk.aws_apigatewayv2_alpha as _apigw
import aws_cdk.aws_apigatewayv2_integrations_alpha as _integrations
from aws_cdk import Aws, Duration, RemovalPolicy
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as logs
from aws_cdk import aws_s3 as _s3
from aws_cdk.aws_apigatewayv2_authorizers_alpha import HttpUserPoolAuthorizer
from cdk_nag import NagSuppressions
from constructs import Construct

QUERY_BEDROCK_TIMEOUT = 900
FEEDBACK_TIMEOUT = 900
PINPOINT_TIMEOUT = 900
S3_TIMEOUT = 900

DIRNAME = os.path.dirname(__file__)


class CDSAIAPIConstructs(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stack_name,
        s3_data_bucket: _s3.Bucket,
        bedrock_region: str,
        pinpoint_project_id: str,
        pinpoint_export_role_arn: str,
        architecture: str,
        python_runtime: str,
        email_identity: str,
        sms_identity: str,
        personalize_role_arn: str,
        personalize_solution_version_arn: str,
        bedrock_role_arn: str = None,
        email_enabled: bool = True,
        sms_enabled: bool = True,
        custom_enabled: bool = True,
        **kwargs,
    ) -> None:
        """Construct for API Gateway.

        Parameters
        ----------
        scope : Construct
            The parent construct.
        construct_id : str
            The identifier of this construct.
        stack_name : str
            The name of the stack.
        s3_data_bucket : _s3.Bucket
            The S3 bucket for storing data.
        bedrock_region : str
            The region for Bedrock.
        pinpoint_project_id : str
            The ID of the Pinpoint project.
        pinpoint_export_role_arn : str
            The ARN of the role for exporting Pinpoint data.
        architecture : str
            The architecture of the Lambda function.
        python_runtime : str
            The Python runtime of the Lambda function.
        email_identity : str
            The email identity for Pinpoint.
        sms_identity : str
            The SMS identity for Pinpoint.
        personalize_role_arn : str
            The ARN of the role for Personalize.
        personalize_solution_version_arn : str
            The ARN of the solution version for Personalize.
        bedrock_role_arn : str, optional
            The ARN of the role for Bedrock.
        email_enabled : bool, optional
            Whether to enable email for Pinpoint.
        sms_enabled : bool, optional
            Whether to enable SMS for Pinpoint.
        custom_enabled : bool, optional
            Whether to enable custom channel for Pinpoint.
        **kwargs
            Additional keyword arguments.

        Attributes
        ----------
        api_uri : str
            The URI of the API Gateway.
        """
        super().__init__(scope, construct_id, **kwargs)

        self.s3_data_bucket = s3_data_bucket
        self.bedrock_region = bedrock_region
        self.bedrock_role_arn = bedrock_role_arn
        self.pinpoint_project_id = pinpoint_project_id
        self.pinpoint_export_role_arn = pinpoint_export_role_arn
        self.email_identity = email_identity
        self.sms_identity = sms_identity
        self.personalize_role_arn = personalize_role_arn
        self.personalize_solution_version_arn = personalize_solution_version_arn
        self.email_enabled = str(email_enabled)
        self.sms_enabled = str(sms_enabled)
        self.custom_enabled = str(custom_enabled)

        # **************** Set Architecture and Python Runtime ****************
        if architecture == "ARM_64":
            self._architecture = _lambda.Architecture.ARM_64
        elif architecture == "X86_64":
            self._architecture = _lambda.Architecture.X86_64
        else:
            raise RuntimeError("Select one option for system architecture among [ARM_64, X86_64]")

        if python_runtime == "PYTHON_3_10":
            self._runtime = _lambda.Runtime.PYTHON_3_10
        elif python_runtime == "PYTHON_3_9":
            self._runtime = _lambda.Runtime.PYTHON_3_9
        elif python_runtime == "PYTHON_3_11":
            self._runtime = _lambda.Runtime.PYTHON_3_11
        else:
            raise RuntimeError("Select a Python version >= PYTHON_3_9")

        # **************** Create resources ****************

        self.create_lambda_layers(stack_name)
        self.create_roles(stack_name)
        self.create_lambda_functions(stack_name)

        self.prefix = stack_name[:16]

        self.create_cognito_user_pool()

        # authorizer = HttpIamAuthorizer()
        authorizer = HttpUserPoolAuthorizer(
            "BooksAuthorizer", self.user_pool, user_pool_clients=[self.user_pool_client]
        )

        # Create the HTTP API with CORS
        http_api = _apigw.HttpApi(
            self,
            f"{stack_name}-http-api",
            default_authorizer=authorizer,
            cors_preflight=_apigw.CorsPreflightOptions(
                allow_methods=[_apigw.CorsHttpMethod.POST],
                allow_origins=["*"],
                max_age=Duration.days(10),
            ),
        )

        # create log group for HTTP API access logging
        logs.LogGroup(self, "ApiGatewayAccessLogs", retention=logs.RetentionDays.ONE_WEEK)

        # set access logging for default stage
        """
        _stage: _apigwv2.CfnStage = http_api.default_stage.node.default_child
        _stage.access_log_settings = _apigwv2.CfnStage.AccessLogSettingsProperty(
            destination_arn=log_group.log_group_arn,
            format="$context.requestId",
        )
        """

        # add content/bedrock to POST /
        http_api.add_routes(
            path="/content/bedrock",
            methods=[_apigw.HttpMethod.POST],
            integration=_integrations.HttpLambdaIntegration(
                "LambdaProxyIntegration", handler=self.bedrock_content_generation_lambda
            ),
        )

        # add Pinpoint segment to GET
        http_api.add_routes(
            path="/pinpoint/segment",
            methods=[_apigw.HttpMethod.GET],
            integration=_integrations.HttpLambdaIntegration(
                "LambdaProxyIntegration", handler=self.pinpoint_segment_lambda
            ),
        )

        # add Pinpoint job to GET / POST
        http_api.add_routes(
            path="/pinpoint/job",
            methods=[_apigw.HttpMethod.GET, _apigw.HttpMethod.POST],
            integration=_integrations.HttpLambdaIntegration("LambdaProxyIntegration", handler=self.pinpoint_job_lambda),
        )

        # add Pinpoint message to POST /
        http_api.add_routes(
            path="/pinpoint/message",
            methods=[_apigw.HttpMethod.POST],
            integration=_integrations.HttpLambdaIntegration(
                "LambdaProxyIntegration", handler=self.pinpoint_message_lambda
            ),
        )

        http_api.add_routes(
            path="/pinpoint/email",
            methods=[_apigw.HttpMethod.POST],
            integration=_integrations.HttpLambdaIntegration(
                "LambdaProxyIntegration", handler=self.pinpoint_message_email_lambda
            ),
        )

        http_api.add_routes(
            path="/pinpoint/sms",
            methods=[_apigw.HttpMethod.POST],
            integration=_integrations.HttpLambdaIntegration(
                "LambdaProxyIntegration", handler=self.pinpoint_message_sms_lambda
            ),
        )

        http_api.add_routes(
            path="/pinpoint/custom",
            methods=[_apigw.HttpMethod.POST],
            integration=_integrations.HttpLambdaIntegration(
                "LambdaProxyIntegration", handler=self.pinpoint_message_custom_lambda
            ),
        )

        # add s3 file to GET /
        http_api.add_routes(
            path="/s3",
            methods=[_apigw.HttpMethod.GET],
            integration=_integrations.HttpLambdaIntegration("LambdaProxyIntegration", handler=self.s3_fetch_lambda),
        )

        # add Personalize batch segment to GET /
        http_api.add_routes(
            path="/personalize/batch-segment-job",
            methods=[_apigw.HttpMethod.GET],
            integration=_integrations.HttpLambdaIntegration(
                "LambdaProxyIntegration", handler=self.personalize_batch_segment_job_lambda
            ),
        )

        # add Personalize batch segment to POST /
        http_api.add_routes(
            path="/personalize/batch-segment-job",
            methods=[_apigw.HttpMethod.POST],
            integration=_integrations.HttpLambdaIntegration(
                "LambdaProxyIntegration", handler=self.personalize_batch_segment_job_lambda
            ),
        )

        # add Personalize batch segments to GET /
        http_api.add_routes(
            path="/personalize/batch-segment-jobs",
            methods=[_apigw.HttpMethod.GET],
            integration=_integrations.HttpLambdaIntegration(
                "LambdaProxyIntegration", handler=self.personalize_batch_segment_jobs_lambda
            ),
        )

        self.api_uri = http_api.api_endpoint

    def create_cognito_user_pool(self):
        # Cognito User Pool
        """Create a Cognito User Pool with advanced security enabled.

        This user pool has the following properties:

        - Auto verification of email
        - MFA required, with only OTP allowed
        - Password policy with the following requirements:
            - Minimum length of 8 characters
            - At least one digit
            - At least one lowercase letter
            - At least one uppercase letter
            - At least one symbol
        - Advanced security mode enabled
        - Removal policy of DESTROY

        Also creates a client application with the following properties:

        - User pool client name is the same as the user pool name
        - No secret is generated
        - Auth flow is user password
        - Client ID is stored in the `client_id` attribute
        """
        self.user_pool = cognito.UserPool(
            self,
            f"{self.prefix}-user-pool",
            user_pool_name=f"{self.prefix}-user-pool",
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            mfa=cognito.Mfa.REQUIRED,
            mfa_second_factor=cognito.MfaSecondFactor(sms=False, otp=True),
            password_policy=cognito.PasswordPolicy(
                min_length=8, require_digits=True, require_lowercase=True, require_uppercase=True, require_symbols=True
            ),
            advanced_security_mode=cognito.AdvancedSecurityMode.ENFORCED,
            removal_policy=RemovalPolicy.DESTROY,
        )

        self.user_pool_client = self.user_pool.add_client(
            "customer-app-client",
            user_pool_client_name=f"{self.prefix}-client",
            generate_secret=False,
            auth_flows=cognito.AuthFlow(user_password=True),
        )

        self.client_id = self.user_pool_client.user_pool_client_id

    ## **************** Lambda Layers ****************
    """
    def create_lambda_layers(self, stack_name):


        self.layer_langchain = _lambda.LayerVersion(
            self,
            f"{stack_name}-langchain-layer",
            compatible_runtimes=[self._runtime],
            compatible_architectures=[self._architecture],
            code=_lambda.Code.from_asset("./assets/layers/langchain/langchain-layer.zip"),
            description="A layer for langchain library",
            layer_version_name=f"{stack_name}-langchain-layer",
        )
    """

    # TODO: Replace python version in code with variable.

    def create_lambda_layers(self, stack_name):
        #        bundling_image = self._runtime.bundling_image
        #        python_version = self._runtime.name.replace("python", "")  # Extracts '3.9' from 'python3.9'
        """Creates layers for langchain and factory_module, and shared_module.

        :param stack_name: The name of the stack.
        :return: None
        """
        self.layer_langchain = _lambda.LayerVersion(
            self,
            f"{stack_name}-langchain-layer",
            compatible_runtimes=[self._runtime],
            compatible_architectures=[self._architecture],
            code=_lambda.Code.from_asset(
                path=os.path.join(".", "assets", "layers", "langchain"),
                bundling={
                    "image": _lambda.Runtime.PYTHON_3_9.bundling_image,
                    #                   "image": bundling_image,
                    "command": [
                        "bash",
                        "-c",
                        "pip install -r requirements.txt "
                        "-t /asset-output/python/lib/python3.9/site-packages/ && "
                        "cp -au . /asset-output",
                    ],
                },
            ),
            description="A layer for langchain library",
            layer_version_name=f"{stack_name}-langchain-layer",
        )

        """
        self.layer_factory_module = _lambda.LayerVersion(
            self,
            f"{stack_name}-factory-module-layer",
            compatible_runtimes=[self._runtime],
            compatible_architectures=[self._architecture],
            code=_lambda.Code.from_asset(
                path=os.path.join(".", "assets", "layers", "factory_module"),
                bundling={
                    "image": _lambda.Runtime.PYTHON_3_9.bundling_image,
                    "command": [
                        "bash", "-c",
                        "cp -au . /asset-output"
                    ],
                },
            ),
            description="A layer for the factory module",
            layer_version_name=f"{stack_name}-factory-module-layer",
        )
        """

        self.layer_factory_module = _lambda.LayerVersion(
            self,
            f"{stack_name}-factory_module-layer",
            compatible_runtimes=[self._runtime],
            compatible_architectures=[self._architecture],
            code=_lambda.Code.from_asset("./assets/layers/factory_module"),
            description="A layer for factory_module",
            layer_version_name=f"{stack_name}-factory_module-layer",
        )

        self.layer_shared_module = _lambda.LayerVersion(
            self,
            f"{stack_name}-shared_module-layer",
            compatible_runtimes=[self._runtime],
            compatible_architectures=[self._architecture],
            #           code=_lambda.Code.from_asset("./assets/python/shared_module"),
            code=_lambda.Code.from_asset("./assets/shared_module"),
            description="A layer for shared code",
            layer_version_name=f"{stack_name}-shared_module-layer",
        )

    # **************** Lambda Functions ****************
    def create_lambda_functions(self, stack_name):
        # ********* Create Marketing Content Bedrock *********
        """Creates the Lambda functions for this stack.

        The functions are created using the given runtime, and are assigned the given
        role and layers. The functions are given the given names, and are given the
        given memory size and timeouts. The functions are also given the given
        environment variables, which are used to configure the functions.

        The functions are created with aliases named "Warm", which are used to
        configure provisioned concurrency for the functions.

        The functions are assigned the following roles:

        - The `bedrock_content_generation_lambda` function is assigned the
        `bedrock_content_generation_role` role.
        - The `pinpoint_segment_lambda` function is assigned the
        `lambda_pinpoint_segment_role` role.
        - The `pinpoint_job_lambda` function is assigned the
        `lambda_pinpoint_job_role` role.
        - The `pinpoint_message_lambda` function is assigned the
        `lambda_pinpoint_message_role` role.
        - The `s3_fetch_lambda` function is assigned the `lambda_s3_role` role.
        - The `personalize_batch_segment_job_lambda` function is assigned the
        `personalize_role` role.
        - The `personalize_batch_segment_jobs_lambda` function is assigned the
        `personalize_role` role.

        :param stack_name: The name of the stack.
        :param runtime: The runtime to use for the functions.
        :param bedrock_content_generation_role: The role to assign to the
        `bedrock_content_generation_lambda` function.
        :param lambda_pinpoint_segment_role: The role to assign to the
        `pinpoint_segment_lambda` function.
        :param lambda_pinpoint_job_role: The role to assign to the
        `pinpoint_job_lambda` function.
        :param lambda_pinpoint_message_role: The role to assign to the
        `pinpoint_message_lambda` function.
        :param lambda_s3_role: The role to assign to the `s3_fetch_lambda`
        function.
        :param personalize_role: The role to assign to the
        `personalize_batch_segment_job_lambda` and
        `personalize_batch_segment_jobs_lambda` functions.
        :param layers: The layers to assign to the functions.
        """

        self.bedrock_content_generation_lambda = _lambda.Function(
            self,
            f"{stack_name}-bedrock-content-generation-lambda",
            runtime=self._runtime,
            code=_lambda.Code.from_asset("./assets/lambda/bedrock_content_generation_lambda"),
            handler="bedrock_content_generation_lambda.lambda_handler",
            architecture=self._architecture,
            function_name=f"{stack_name}-bedrock-content-generation-lambda",
            memory_size=3008,
            timeout=Duration.seconds(QUERY_BEDROCK_TIMEOUT),
            environment={
                "BUCKET_NAME": self.s3_data_bucket.bucket_name,
                "BEDROCK_REGION": self.bedrock_region,
                "BEDROCK_ROLE_ARN": str(self.bedrock_role_arn),
            },
            role=self.bedrock_content_generation_role,
            layers=[self.layer_langchain],
        )
        self.bedrock_content_generation_lambda.add_alias(
            "Warm",
            provisioned_concurrent_executions=0,
            description="Alias used for Lambda provisioned concurrency",
        )

        # ********* Pinpoint Segment *********
        self.pinpoint_segment_lambda = _lambda.Function(
            self,
            f"{stack_name}-pinpoint-segment-lambda",
            runtime=self._runtime,
            code=_lambda.Code.from_asset("./assets/lambda/genai_pinpoint_segment"),
            handler="pinpoint_segment.lambda_handler",
            function_name=f"{stack_name}-pinpoint-segment",
            memory_size=3008,
            timeout=Duration.seconds(PINPOINT_TIMEOUT),
            environment={
                "PINPOINT_PROJECT_ID": self.pinpoint_project_id,
            },
            role=self.lambda_pinpoint_segment_role,
        )
        self.pinpoint_segment_lambda.add_alias(
            "Warm",
            provisioned_concurrent_executions=0,
            description="Alias used for Lambda provisioned concurrency",
        )

        # ********* Pinpoint Job *********
        self.pinpoint_job_lambda = _lambda.Function(
            self,
            f"{stack_name}-pinpoint-job-lambda",
            runtime=self._runtime,
            code=_lambda.Code.from_asset("./assets/lambda/genai_pinpoint_job"),
            handler="pinpoint_job.lambda_handler",
            function_name=f"{stack_name}-pinpoint-job",
            memory_size=3008,
            timeout=Duration.seconds(PINPOINT_TIMEOUT),
            environment={
                "PINPOINT_PROJECT_ID": self.pinpoint_project_id,
                "PINPOINT_EXPORT_ROLE_ARN": self.pinpoint_export_role_arn,
                "BUCKET_NAME": self.s3_data_bucket.bucket_name,
            },
            role=self.lambda_pinpoint_job_role,
        )
        self.pinpoint_job_lambda.add_alias(
            "Warm",
            provisioned_concurrent_executions=0,
            description="Alias used for Lambda provisioned concurrency",
        )

        # ********* Pinpoint Message *********
        self.pinpoint_message_lambda = _lambda.Function(
            self,
            f"{stack_name}-pinpoint-message-lambda",
            runtime=self._runtime,
            code=_lambda.Code.from_asset("./assets/lambda/genai_pinpoint_message"),
            handler="pinpoint_message.lambda_handler",
            function_name=f"{stack_name}-pinpoint-message",
            memory_size=3008,
            timeout=Duration.seconds(PINPOINT_TIMEOUT),
            environment={
                "PINPOINT_PROJECT_ID": self.pinpoint_project_id,
                "BUCKET_NAME": self.s3_data_bucket.bucket_name,
                "EMAIL_IDENTITY": self.email_identity,
                "SMS_IDENTITY": self.sms_identity,
                "EMAIL_ENABLED": self.email_enabled,
                "SMS_ENABLED": self.sms_enabled,
                "CUSTOM_ENABLED": self.custom_enabled,
            },
            role=self.lambda_pinpoint_message_role,
            # FAS Attached the Layer - because of need for the requests_toolbelt module.
            layers=[self.layer_langchain],
        )
        self.pinpoint_message_lambda.add_alias(
            "Warm",
            provisioned_concurrent_executions=0,
            description="Alias used for Lambda provisioned concurrency",
        )

        self.pinpoint_message_email_lambda = _lambda.Function(
            self,
            f"{stack_name}-pinpoint-message-email-lambda",
            runtime=self._runtime,
            code=_lambda.Code.from_asset("./assets/lambda/genai_pinpoint_message_email"),
            handler="pinpoint_message_email.lambda_handler",
            function_name=f"{stack_name}-pinpoint-message-email",
            memory_size=3008,
            timeout=Duration.seconds(PINPOINT_TIMEOUT),
            environment={
                "PINPOINT_PROJECT_ID": self.pinpoint_project_id,
                "BUCKET_NAME": self.s3_data_bucket.bucket_name,
                "EMAIL_IDENTITY": self.email_identity,
                "SMS_IDENTITY": self.sms_identity,
                "EMAIL_ENABLED": self.email_enabled,
                "SMS_ENABLED": self.sms_enabled,
                "CUSTOM_ENABLED": self.custom_enabled,
            },
            role=self.lambda_pinpoint_message_role,
            # FAS Attached the Layer - because of need for the requests_toolbelt module.
            layers=[
                self.layer_langchain,
                self.layer_factory_module,
                self.layer_shared_module,
            ],
        )

        self.pinpoint_message_email_lambda.add_alias(
            "Warm",
            provisioned_concurrent_executions=0,
            description="Alias used for Lambda provisioned concurrency",
        )

        self.pinpoint_message_sms_lambda = _lambda.Function(
            self,
            f"{stack_name}-pinpoint-message-sms-lambda",
            runtime=self._runtime,
            code=_lambda.Code.from_asset("./assets/lambda/genai_pinpoint_message_sms"),
            handler="pinpoint_message_sms.lambda_handler",
            function_name=f"{stack_name}-pinpoint-message-sms",
            memory_size=3008,
            timeout=Duration.seconds(PINPOINT_TIMEOUT),
            environment={
                "PINPOINT_PROJECT_ID": self.pinpoint_project_id,
                "BUCKET_NAME": self.s3_data_bucket.bucket_name,
                "EMAIL_IDENTITY": self.email_identity,
                "SMS_IDENTITY": self.sms_identity,
                "EMAIL_ENABLED": self.email_enabled,
                "SMS_ENABLED": self.sms_enabled,
                "CUSTOM_ENABLED": self.custom_enabled,
            },
            role=self.lambda_pinpoint_message_role,
            # FAS Attached the Layer - because of need for the requests_toolbelt module.
            layers=[
                self.layer_langchain,
                self.layer_factory_module,
                self.layer_shared_module,
            ],
        )
        self.pinpoint_message_sms_lambda.add_alias(
            "Warm",
            provisioned_concurrent_executions=0,
            description="Alias used for Lambda provisioned concurrency",
        )

        self.pinpoint_message_custom_lambda = _lambda.Function(
            self,
            f"{stack_name}-pinpoint-message-custom-lambda",
            runtime=self._runtime,
            code=_lambda.Code.from_asset("./assets/lambda/genai_pinpoint_message_custom"),
            handler="pinpoint_message_custom.lambda_handler",
            function_name=f"{stack_name}-pinpoint-message-custom",
            memory_size=3008,
            timeout=Duration.seconds(PINPOINT_TIMEOUT),
            environment={
                "PINPOINT_PROJECT_ID": self.pinpoint_project_id,
                "BUCKET_NAME": self.s3_data_bucket.bucket_name,
                "custom_IDENTITY": self.email_identity,
                "SMS_IDENTITY": self.sms_identity,
                "EMAIL_ENABLED": self.email_enabled,
                "SMS_ENABLED": self.sms_enabled,
                "CUSTOM_ENABLED": self.custom_enabled,
            },
            role=self.lambda_pinpoint_message_role,
            # FAS Attached the Layer - because of need for the requests_toolbelt module.
            layers=[
                self.layer_langchain,
                self.layer_factory_module,
                self.layer_shared_module,
            ],
        )

        self.pinpoint_message_custom_lambda.add_alias(
            "Warm",
            provisioned_concurrent_executions=0,
            description="Alias used for Lambda provisioned concurrency",
        )

        # ********* S3 Fetch *********
        self.s3_fetch_lambda = _lambda.Function(
            self,
            f"{stack_name}-s3-fetch-lambda",
            runtime=self._runtime,
            code=_lambda.Code.from_asset("./assets/lambda/genai_s3"),
            handler="s3_fetch.lambda_handler",
            function_name=f"{stack_name}-s3-fetch",
            memory_size=3008,
            timeout=Duration.seconds(S3_TIMEOUT),
            environment={
                "BUCKET_NAME": self.s3_data_bucket.bucket_name,
            },
            role=self.lambda_s3_role,
        )
        self.s3_fetch_lambda.add_alias(
            "Warm",
            provisioned_concurrent_executions=0,
            description="Alias used for Lambda provisioned concurrency",
        )

        # ********* Personalize *********

        # ********* Personalize Batch Segment Job *********
        self.personalize_batch_segment_job_lambda = _lambda.Function(
            self,
            f"{stack_name}-personalize-batch-segment-job-lambda",
            runtime=self._runtime,
            code=_lambda.Code.from_asset("./assets/lambda/genai_personalize_batch_segment_job"),
            handler="personalize_batch_segment_job.lambda_handler",
            function_name=f"{stack_name}-personalize-batch-segment-job",
            memory_size=3008,
            timeout=Duration.seconds(S3_TIMEOUT),
            environment={
                "BUCKET_NAME": self.s3_data_bucket.bucket_name,
                "PERSONALIZE_ROLE_ARN": self.personalize_role_arn,
                "SOLUTION_VERSION_ARN": self.personalize_solution_version_arn,
            },
            role=self.personalize_role,
        )
        self.personalize_batch_segment_job_lambda.add_alias(
            "Warm",
            provisioned_concurrent_executions=0,
            description="Alias used for Lambda provisioned concurrency",
        )

        # ********* Personalize Batch Segment Jobs *********
        self.personalize_batch_segment_jobs_lambda = _lambda.Function(
            self,
            f"{stack_name}-personalize-batch-segment-jobs-lambda",
            runtime=self._runtime,
            code=_lambda.Code.from_asset("./assets/lambda/genai_personalize_batch_segment_jobs"),
            handler="personalize_batch_segment_jobs.lambda_handler",
            function_name=f"{stack_name}-personalize-batch-segment-jobs",
            memory_size=3008,
            timeout=Duration.seconds(S3_TIMEOUT),
            role=self.personalize_role,
        )
        self.personalize_batch_segment_jobs_lambda.add_alias(
            "Warm",
            provisioned_concurrent_executions=0,
            description="Alias used for Lambda provisioned concurrency",
        )

    # TODO: Separate roles for 3 message lambdas.
    # **************** IAM Permissions ****************
    def create_roles(self, stack_name: str):
        # ********* IAM Roles *********
        """Creates the IAM Roles and Policies for the various Lambda functions,
        API Gateway, and Personalize.

        :param stack_name: The name of the CDK Stack
        :return: None
        """
        self.bedrock_content_generation_role = iam.Role(
            self,
            f"{stack_name}-bedrock-content-generation-role",
            role_name=f"{stack_name}-bedrock-content-generation-role",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("lambda.amazonaws.com"),
            ),
        )
        self.lambda_pinpoint_segment_role = iam.Role(
            self,
            f"{stack_name}-pinpoint-segment-role",
            role_name=f"{stack_name}-pinpoint-segment-role",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("lambda.amazonaws.com"),
            ),
        )
        self.lambda_pinpoint_job_role = iam.Role(
            self,
            f"{stack_name}-pinpoint-job-role",
            role_name=f"{stack_name}-pinpoint-job-role",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("lambda.amazonaws.com"),
            ),
        )
        self.lambda_pinpoint_message_role = iam.Role(
            self,
            f"{stack_name}-pinpoint-message-role",
            role_name=f"{stack_name}-pinpoint-message-role",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("lambda.amazonaws.com"),
            ),
        )
        self.lambda_s3_role = iam.Role(
            self,
            f"{stack_name}-s3-role",
            role_name=f"{stack_name}-s3-role",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("lambda.amazonaws.com"),
            ),
        )

        self.personalize_role = iam.Role(
            self,
            f"{stack_name}-personalize-role",
            role_name=f"{stack_name}-personalize-role",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("lambda.amazonaws.com"),
            ),
        )

        # ********* Lambda Basic Execution Role *********
        cloudwatch_access_docpolicy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "logs:*",
                    ],
                    resources=["*"],
                )
            ]
        )

        iam.Policy(
            self,
            f"{stack_name}-cloudwatch-access-policy",
            policy_name=f"{stack_name}-cloudwatch-access-policy",
            document=cloudwatch_access_docpolicy,
        )

        self.bedrock_content_generation_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )
        self.lambda_pinpoint_segment_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )
        self.lambda_pinpoint_job_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )
        self.lambda_pinpoint_message_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )
        self.lambda_s3_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )
        self.personalize_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )

        # ********* Bedrock *********
        if self.bedrock_role_arn is None:
            bedrock_access_docpolicy = iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        actions=[
                            "bedrock:ListFoundationModels",
                            "bedrock:GetFoundationModel",
                            "bedrock:InvokeModel",
                        ],
                        resources=["*"],
                    )
                ]
            )

        else:
            bedrock_access_docpolicy = iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        actions=[
                            "sts:AssumeRole",
                        ],
                        resources=[self.bedrock_role_arn],
                    )
                ]
            )
            bedrock_access_docpolicy = iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        actions=[
                            "sts:AssumeRole",
                        ],
                        resources=[self.bedrock_role_arn],
                    ),
                    iam.PolicyStatement(
                        actions=[
                            "bedrock:*",
                        ],
                        resources=["*"],
                    ),
                ]
            )

        bedrock_access_policy = iam.Policy(
            self,
            f"{stack_name}-bedrock-access-policy",
            policy_name=f"{stack_name}-bedrock-access-policy",
            document=bedrock_access_docpolicy,
        )

        self.bedrock_content_generation_role.attach_inline_policy(bedrock_access_policy)

        # ********* S3 Access *********
        self.s3_data_bucket.grant_read_write(self.lambda_pinpoint_segment_role)
        self.s3_data_bucket.grant_read_write(self.lambda_pinpoint_message_role)
        self.s3_data_bucket.grant_read_write(self.personalize_role)
        self.s3_data_bucket.grant_read(self.lambda_s3_role)
        # Grant Amazon Personalize the required permissions on the bucket
        self.s3_data_bucket.grant_read_write(iam.ServicePrincipal("personalize.amazonaws.com"))

        # ********* Pinpoint Access *********
        # Inline Statement to allow get-segments on a specific Pinpoint project
        pinpoint_segment_policy_statement = iam.PolicyStatement(
            actions=["mobiletargeting:GetSegments"],
            resources=[f"arn:aws:mobiletargeting:{Aws.REGION}:{Aws.ACCOUNT_ID}:apps/{self.pinpoint_project_id}"],
            effect=iam.Effect.ALLOW,
        )
        pinpoint_segment_policy = iam.Policy(
            self,
            id=f"{stack_name}-pinpoint-segment-acess-policy",
            policy_name=f"{stack_name}-pinpoint-segment-acess-policy",
            statements=[pinpoint_segment_policy_statement],
        )

        pinpoint_segment_policy.attach_to_role(self.lambda_pinpoint_segment_role)

        # Statement to allow Getting Export Job from Pinpoint
        pinpoint_export_job_policy_statement = iam.PolicyStatement(
            actions=["mobiletargeting:GetExportJob"], resources=["*"], effect=iam.Effect.ALLOW
        )
        # Statement to allow creating Pinpoint Export Job
        pinpoint_create_export_job_policy_statement = iam.PolicyStatement(
            actions=["mobiletargeting:CreateExportJob"],
            resources=[f"arn:aws:mobiletargeting:{Aws.REGION}:{Aws.ACCOUNT_ID}:apps/{self.pinpoint_project_id}"],
            effect=iam.Effect.ALLOW,
        )
        # Statement to allow passing the Pinpoint S3 Role to Pinpoint
        pinpoint_pass_export_role_policy_statement = iam.PolicyStatement(
            actions=["iam:PassRole"], resources=[self.pinpoint_export_role_arn], effect=iam.Effect.ALLOW
        )
        pinpoint_export_job_policy = iam.Policy(
            self,
            id=f"{stack_name}-pinpoint-export-job-policy",
            policy_name=f"{stack_name}-pinpoint-export-job-policy",
            statements=[
                pinpoint_export_job_policy_statement,
                pinpoint_create_export_job_policy_statement,
                pinpoint_pass_export_role_policy_statement,
            ],
        )

        pinpoint_export_job_policy.attach_to_role(self.lambda_pinpoint_job_role)

        # Allow sending message through Pinpoint
        pinpoint_send_message_policy_statement = iam.PolicyStatement(
            actions=["mobiletargeting:SendMessages", "mobiletargeting:SendUsersMessages"],
            resources=[
                f"arn:aws:mobiletargeting:{Aws.REGION}:{Aws.ACCOUNT_ID}:apps/{self.pinpoint_project_id}/messages"
            ],
            effect=iam.Effect.ALLOW,
        )
        pinpoint_send_sms_voice_policy_statement = iam.PolicyStatement(
            actions=["sms-voice:SendTextMessage", "sms-voice:SendVoiceMessage"],
            resources=[f"arn:aws:sms-voice:{Aws.REGION}:{Aws.ACCOUNT_ID}:phone-number/{self.sms_identity}"],
            effect=iam.Effect.ALLOW,
        )

        # FAS: Needed to define a policy statement that gives the Lambda
        # permission to access the SES Identity.

        # Create a policy statement for SES email sending with a specific ARN
        #
        pinpoint_ses_send_email_policy_statement = iam.PolicyStatement(
            actions=["ses:SendEmail", "ses:SendRawEmail"],
            resources=[f"arn:aws:ses:{Aws.REGION}:{Aws.ACCOUNT_ID}:identity/{self.email_identity}"],
            effect=iam.Effect.ALLOW,
        )

        pinpoint_send_message_policy = iam.Policy(
            self,
            id=f"{stack_name}-pinpoint-send-message-policy",
            policy_name=f"{stack_name}-pinpoint-send-message-policy",
            statements=[
                pinpoint_send_message_policy_statement,
                pinpoint_send_sms_voice_policy_statement,
                pinpoint_ses_send_email_policy_statement,
            ],
            #    statements=[pinpoint_send_message_policy_statement, pinpoint_send_sms_voice_policy_statement],
        )

        pinpoint_send_message_policy.attach_to_role(self.lambda_pinpoint_message_role)

        # ********* Personalize Access *********
        # Add Personalize Full Access to the Lambda function
        self.personalize_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonPersonalizeFullAccess")
        )

        # ********* CDK Nag Suppressions *********

        NagSuppressions.add_resource_suppressions(
            bedrock_access_policy,
            [{"id": "AwsSolutions-IAM5", "reason": "Already configured action to least privilege"}],
            apply_to_children=True,
        )

        NagSuppressions.add_resource_suppressions(
            self.lambda_pinpoint_segment_role,
            [{"id": "AwsSolutions-IAM5", "reason": "Policy for Lambda to access S3 so wildcards are acceptable"}],
            apply_to_children=True,
        )

        NagSuppressions.add_resource_suppressions(
            self.lambda_pinpoint_message_role,
            [{"id": "AwsSolutions-IAM5", "reason": "Policy for Lambda to access S3 so wildcards are acceptable"}],
            apply_to_children=True,
        )

        NagSuppressions.add_resource_suppressions(
            pinpoint_export_job_policy,
            [{"id": "AwsSolutions-IAM5", "reason": "Policy for Pinpoint to export to S3 so wildcards are acceptable"}],
            apply_to_children=True,
        )

        NagSuppressions.add_resource_suppressions(
            self.lambda_s3_role,
            [{"id": "AwsSolutions-IAM5", "reason": "Policy for Lambda to access S3 so wildcards are acceptable"}],
            apply_to_children=True,
        )

        NagSuppressions.add_resource_suppressions(
            self.personalize_role,
            [
                {
                    "id": "AwsSolutions-IAM5",
                    "reason": "Policy for Personalize Lambda to access S3 so wildcards are acceptable",
                },
                {
                    "id": "AwsSolutions-IAM4",
                    "reason": "Policy for Personalize Lambda to access S3 so using managed policy",
                },
            ],
            apply_to_children=True,
        )
