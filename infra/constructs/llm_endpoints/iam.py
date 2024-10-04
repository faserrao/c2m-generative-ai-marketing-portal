"""This module contains classes for creating IAM roles for SageMaker Endpoints.

The `SageMakerEndpointBasicExecutionRole` class defines an IAM role with
the minimum set of permissions required for SageMaker Endpoints to
function. It is given permission to create and write to CloudWatch logs.
"""

from __future__ import annotations

import re
from pathlib import Path

from aws_cdk import aws_iam as iam
from constructs import Construct

from infra.constructs.llm_endpoints.constants import NAME_SEPARATOR


class SageMakerEndpointBasicExecutionRole(Construct):
    def __init__(self, scope: Construct, construct_id: str, resource_prefix: str) -> None:
        """Construct an IAM role for SageMaker Endpoints to use.

        The role is given the minimum set of permissions required for SageMaker Endpoints to function.
        In particular, it is given permission to create and write to CloudWatch logs.

        Parameters
        ----------
        scope : Construct
            The scope in which to define this construct.
        construct_id : str
            The ID of this construct.
        resource_prefix : str
            The prefix to use for the name of the IAM role.
        """
        super().__init__(scope=scope, id=construct_id)

        # See https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html#sagemaker-roles-createmodel-perms
        base_cw_permissions_policy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "cloudwatch:PutMetricData",
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:DescribeLogStreams",
                        "logs:PutLogEvents",
                    ],
                    resources=["*"],
                )
            ]
        )

        self.role = iam.Role(
            scope=self,
            id=construct_id,
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
            inline_policies={"SageMakerEndpointBasicLoggingPolicy": base_cw_permissions_policy},
            role_name=NAME_SEPARATOR.join([resource_prefix, "endpoint", "execution", "role"]),
        )

    @property
    def arn(self) -> str:
        return self.role.role_arn


class ModelArtifactsAccessGrantor(Construct):
    ALLOWED_BUCKET_ACTIONS = [
        "s3:ListBucket",
    ]

    ALLOWED_OBJECTS_ACTIONS = [
        "s3:GetObject",
    ]

    def __init__(
        self, scope: Construct, construct_id: str, *, bucket_name: str, prefix: str, resource_prefix: str
    ) -> None:
        """Grant a role access to read model artifacts from S3.

        :param scope: The construct scope.
        :param construct_id: The construct ID.
        :param bucket_name: The name of the S3 bucket.
        :param prefix: The prefix of the objects in the S3 bucket.
        :param resource_prefix: The prefix used to name the resources.
        """
        super().__init__(scope=scope, id=construct_id)
        prefix = Path(prefix)
        if prefix.suffixes:
            objects = prefix.as_posix()
        else:
            objects = f"{prefix.parent.as_posix()}/*"

        self._artifacts_policy = iam.Policy(
            scope=self,
            id="ReadPolicy",
            statements=[
                iam.PolicyStatement(
                    actions=self.ALLOWED_BUCKET_ACTIONS,
                    effect=iam.Effect.ALLOW,
                    resources=[f"arn:aws:s3:::{bucket_name}"],
                ),
                iam.PolicyStatement(
                    actions=self.ALLOWED_OBJECTS_ACTIONS,
                    effect=iam.Effect.ALLOW,
                    resources=[f"arn:aws:s3:::{bucket_name}/{objects}"],
                ),
            ],
            policy_name=NAME_SEPARATOR.join([resource_prefix, "endpoint", "model", "artifacts", "access", "policy"]),
        )

    @classmethod
    def from_uri(
        cls, scope: Construct, construct_id: str, uri: str, resource_prefix: str
    ) -> ModelArtifactsAccessGrantor:
        """Create an instance of ModelArtifactsAccessGrantor from an S3 URI.

        Parameters
        ----------
        scope : Construct
            The scope in which to define this construct.
        construct_id : str
            The ID of this construct.
        uri : str
            The URI of the S3 bucket.
        resource_prefix : str
            The prefix used to name the resources.

        Returns
        -------
        ModelArtifactsAccessGrantor
            The ModelArtifactsAccessGrantor instance.
        """
        bucket_name, prefix = re.search(r"^s3://(.+)", uri).group(1).split("/", 1)
        return cls(
            scope=scope,
            construct_id=construct_id,
            bucket_name=bucket_name,
            prefix=prefix,
            resource_prefix=resource_prefix,
        )

    def grant_read(self, role: iam.IRole) -> None:
        """Grant a role read access to the model artifacts in the S3 bucket.

        Parameters
        ----------
        role : iam.IRole
            The IAM role to grant read access to.
        """
        role.attach_inline_policy(policy=self._artifacts_policy)


class ImageRepositoryAccessGrantor(Construct):
    AUTHENTICATION_ACTIONS = [
        "ecr:GetAuthorizationToken",
    ]
    ALLOWED_READ_ACTIONS = [
        "ecr:BatchCheckLayerAvailability",
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer",
    ]

    def __init__(self, scope: Construct, construct_id: str, *, arn: str, resource_prefix: str) -> None:
        """Create an instance of ImageRepositoryAccessGrantor.

        Parameters
        ----------
        scope : Construct
            The scope in which to define this construct.
        construct_id : str
            The ID of this construct.
        arn : str
            The ARN of the Amazon ECR image repository.
        resource_prefix : str
            The prefix used to name the resources.
        """
        super().__init__(scope=scope, id=construct_id)
        self.arn = arn
        self._pull_policy = iam.Policy(
            scope=self,
            id="PullPolicy",
            statements=[
                iam.PolicyStatement(actions=self.AUTHENTICATION_ACTIONS, effect=iam.Effect.ALLOW, resources=["*"]),
                iam.PolicyStatement(
                    actions=self.ALLOWED_READ_ACTIONS, effect=iam.Effect.ALLOW, resources=[f"{self.arn}*"]
                ),
            ],
            policy_name=NAME_SEPARATOR.join([resource_prefix, "endpoint", "image", "access", "policy"]),
        )

    @classmethod
    def from_uri(
        cls, scope: Construct, construct_id: str, uri: str, resource_prefix: str
    ) -> ImageRepositoryAccessGrantor:
        """Create an instance of ImageRepositoryAccessGrantor from a Docker
        image URI.

        Parameters
        ----------
        scope : Construct
            The scope in which to define this construct.
        construct_id : str
            The ID of this construct.
        uri : str
            The URI of the Docker image.
        resource_prefix : str
            The prefix used to name the resources.

        Returns
        -------
        ImageRepositoryAccessGrantor
            An instance of ImageRepositoryAccessGrantor.
        """
        account, region_name, repo_name = re.search(r"^([0-9]+).dkr.ecr.([a-z0-9-]+).amazonaws.com/(.+):", uri).groups()
        return cls(
            scope=scope,
            construct_id=construct_id,
            arn=f"arn:aws:ecr:{region_name}:{account}:repository/{repo_name}",
            resource_prefix=resource_prefix,
        )

    def grant_pull(self, role: iam.IRole) -> None:
        """Grant a role pull access to the ECR repository.

        Parameters
        ----------
        role : iam.IRole
            The IAM role to grant pull access to.
        """
        role.attach_inline_policy(policy=self._pull_policy)
