import os
from pathlib import Path

import aws_cdk as cdk
import yaml
from cdk_nag import NagSuppressions
from yaml.loader import SafeLoader

from infra.cdsgenai_stack import CDSGenAIStack

with open(os.path.join(Path(__file__).parent, "config.yml"), "r", encoding="utf-8") as ymlfile:
    stack_config = yaml.load(ymlfile, Loader=SafeLoader)

app = cdk.App()
env = cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION"))
stack = CDSGenAIStack(scope=app, stack_name=stack_config["stack_name"], config=stack_config, env=env)

# Apply CDK-nag (un-comment to view CDK nag outputs and modify accordingly)
# Aspects.of(app).add(AwsSolutionsChecks())

NagSuppressions.add_stack_suppressions(
    stack,
    [
        {
            "id": "AwsSolutions-IAM5",
            "reason": "BucketDeployment only used to deploy sample data to s3",
        },
        {
            "id": "AwsSolutions-IAM4",
            "reason": "BucketDeployment only used to deploy sample data to s3",
        },
        {
            "id": "AwsSolutions-L1",
            "reason": "BucketDeployment only used to deploy sample data to s3",
        },
    ],
    apply_to_nested_stacks=True,
)

app.synth()
