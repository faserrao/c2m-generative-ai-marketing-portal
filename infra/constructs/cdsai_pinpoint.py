"""CDSGenAI Pinpoint Construct."""

from aws_cdk import Aws
from aws_cdk import aws_iam as iam
from aws_cdk import aws_pinpoint as pinpoint
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3_deploy
from aws_cdk import aws_ses as ses
from cdk_nag import NagSuppressions
from constructs import Construct


class PinpointConstructs(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stack_name: str,
        create_project: bool,
        project_id: str,
        email_identity: str,
        sms_identity: str,
        s3_data_bucket=s3.Bucket,
        **kwargs,
    ) -> None:
        """Construct for Pinpoint.

        Parameters
        ----------
        scope : Construct
            The parent construct.
        construct_id : str
            The identifier of this construct.
        stack_name : str
            The name of the stack.
        create_project : bool
            Whether to create a Pinpoint Project or use an existing one.
        project_id : str
            The ID of the Pinpoint project.
        email_identity : str
            The email identity for Pinpoint.
        sms_identity : str
            The SMS identity for Pinpoint.
        s3_data_bucket : s3.Bucket
            The S3 bucket for storing data. Default is an empty s3.Bucket object.

        Returns
        -------
        None
        """
        super().__init__(scope, construct_id, **kwargs)

        self.pinpoint_project_id = self.create_pinpoint_project(create_project, project_id)
        self.pinpoint_role_ARN = self.grant_pinpoint_s3_export(s3_data_bucket, self.pinpoint_project_id)
        self.deployed_bucket = self.upload_sample_segment_s3(s3_data_bucket)
        self.setup_email_identity(email_identity)
        self.setup_sms_channel()

    def create_pinpoint_project(self, create_project, project_id=None):
        # Initialize Pinpoint Project or get project ID
        """Initialize Pinpoint Project or get project ID.

        Parameters
        ----------
        create_project : bool
            Whether to create a Pinpoint Project or use an existing one.
        project_id : str, optional
            The ID of the Pinpoint project. Default is None.

        Returns
        -------
        str
            The ID of the Pinpoint project.
        """
        if create_project:
            pinpoint_project = pinpoint.CfnApp(self, id="cds-ai-pinpoint", name="cds-ai-pinpoint")
            return pinpoint_project.ref
        return project_id

    def grant_pinpoint_s3_export(self, bucket, project_id):
        # Define the IAM policy
        """Grant Pinpoint the necessary permissions to export data to an S3
        bucket.

        Parameters
        ----------
        bucket : s3.Bucket
            The S3 bucket to which Pinpoint should export data.
        project_id : str
            The ID of the Pinpoint project.

        Returns
        -------
        str
            The ARN of the IAM role that has been created and assigned the necessary permissions.
        """
        export_policy_document = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    sid="AllowUserToSeeBucketListInTheConsole",
                    actions=["s3:ListAllMyBuckets", "s3:GetBucketLocation"],
                    effect=iam.Effect.ALLOW,
                    resources=["arn:aws:s3:::*"],
                ),
                iam.PolicyStatement(
                    sid="AllowAllS3ActionsInBucket",
                    actions=["s3:*"],
                    effect=iam.Effect.ALLOW,
                    resources=[bucket.bucket_arn, f"{bucket.bucket_arn}/*"],
                ),
            ]
        )

        # Create the IAM policy
        pinpoint_policy = iam.ManagedPolicy(self, "s3ExportPolicy", document=export_policy_document)

        NagSuppressions.add_resource_suppressions(
            pinpoint_policy,
            [{"id": "AwsSolutions-IAM5", "reason": "Policy for Pinpoint service so wildcards are acceptable"}],
        )

        # Define the trust relationship
        trust_relationship = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["sts:AssumeRole"],
            principals=[iam.ServicePrincipal("pinpoint.amazonaws.com")],
            conditions={
                "ArnLike": {"aws:SourceArn": f"arn:aws:mobiletargeting:{Aws.REGION}:{Aws.ACCOUNT_ID}:apps/{project_id}"}
            },
        )

        # Create the IAM role and attach the policy
        pinpoint_role = iam.Role(
            self,
            "s3ExportRole",
            assumed_by=iam.PrincipalWithConditions(
                iam.ServicePrincipal("pinpoint.amazonaws.com"), trust_relationship.conditions
            ),
        )

        pinpoint_role.add_managed_policy(pinpoint_policy)

        return pinpoint_role.role_arn

    def upload_sample_segment_s3(self, bucket):
        # Deploy Sample File onto Buckets
        """Deploys the sample Pinpoint user segment data onto the provided S3
        bucket.

        Parameters
        ----------
        bucket : s3.Bucket
            The S3 bucket onto which the sample segment data should be deployed.

        Returns
        -------
        s3_deploy.BucketDeployment
            The deployed bucket with the sample segment data.
        """
        pinpoint_sample_segment_deployment = s3_deploy.BucketDeployment(
            self,
            "s3_segment_sample_file_deployment",
            destination_bucket=bucket,
            sources=[s3_deploy.Source.asset("./assets/demo-data")],
            destination_key_prefix="demo-data/",
            retain_on_delete=False,
        )

        return pinpoint_sample_segment_deployment.deployed_bucket

    def setup_email_identity(self, email_identity):
        # First verify the email identity with Amazon SES
        """Verifies an email identity with Amazon SES and enables the email
        channel with Amazon Pinpoint.

        Parameters
        ----------
        email_identity : str
            The email address to be verified and enabled with Amazon Pinpoint.

        Returns
        -------
        pinpoint.CfnEmailChannel
            The enabled Amazon Pinpoint Email Channel.
        """

        identity = ses.EmailIdentity(self, "email_identity", identity=ses.Identity.email(email_identity))

        # Enable Amazon Pinpoint Email Channel

        return pinpoint.CfnEmailChannel(
            self,
            "pinpoint_email_channel",
            application_id=self.pinpoint_project_id,
            from_address=email_identity,
            identity=f"arn:aws:ses:{Aws.REGION}:{Aws.ACCOUNT_ID}:identity/{identity.email_identity_name}",
            enabled=True,
        )

    def setup_sms_channel(self):
        # Enable Amazon Pinpoint SMS Channel
        """Enables the Amazon Pinpoint SMS Channel.

        Returns
        -------
        pinpoint.CfnSMSChannel
            The enabled Amazon Pinpoint SMS Channel.
        """
        return pinpoint.CfnSMSChannel(
            self,
            "pinpoint_sms_channel",
            application_id=self.pinpoint_project_id,
            enabled=True,
        )
