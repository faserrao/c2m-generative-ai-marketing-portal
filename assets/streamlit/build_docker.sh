# Configure Account and region
# FAS Modified this file to not use 'latest as the IMAGE_TAG'
# This may be the reason why the nested cloudformation stack
# ends up being run every time.  This is the stack that defines
# the ECS objects and is the reason the stack hangs.  So if
# we want to avoid running it if possible.

AWS_ACCOUNT_ID=$1
AWS_REGION='us-east-1'

IMAGE_TAG='v1.0'  # Use versioned tags
ECR_REPOSITORY='cdk-hnb659fds-container-assets-454674044397-us-east-1'
# ECR_REPOSITORY='public.ecr.aws/v1a3q6c0/streamlit-temp-stack:latest'
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/v1a3q6c0
docker build . --tag $IMAGE_TAG
docker tag $IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG
eval $(aws ecr get-login --no-include-email)
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG