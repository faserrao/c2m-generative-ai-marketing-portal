from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_logs as logs,
    Duration
)
from constructs import Construct

class MyEcsService(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Define ECS Cluster
        cluster = ecs.Cluster(self, "MyCluster", vpc=ec2.Vpc(self, "MyVpc"))

        # Define Fargate Task Definition
        fargate_task_definition = ecs.FargateTaskDefinition(
            self, "WebappTaskDef", memory_limit_mib=512, cpu=256
        )

        fargate_task_definition.add_container(
            "WebContainer",
            image=ecs.ContainerImage.from_docker_image_asset(self.docker_asset),
            port_mappings=[ecs.PortMapping(container_port=8501, protocol=ecs.Protocol.TCP)],
            logging=ecs.LogDrivers.aws_logs(stream_prefix="WebContainerLogs"),
            environment={
                "CLIENT_ID": "example-client-id",
                "API_URI": "https://api.example.com",
                "BUCKET_NAME": "my-s3-bucket"
            },
            health_check=ecs.HealthCheck(
                command=["CMD-SHELL", "curl -f http://localhost:8501/ || exit 1"],
                interval=Duration.seconds(60),
                timeout=Duration.seconds(10),
                retries=3,
                start_period=Duration.seconds(120)
            )
        )

        # Define Fargate Service with desired task count
        service = ecs.FargateService(
            self,
            "StreamlitECSService",
            cluster=cluster,
            task_definition=fargate_task_definition,
            desired_count=3,  # Set the desired number of tasks
            service_name="stl-front",
            security_groups=[ec2.SecurityGroup(self, "MySecurityGroup", vpc=ec2.Vpc(self, "MyVpc"))],
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            health_check_grace_period=Duration.seconds(300),
        )


service = ecs.FargateService(
    self,
    "StreamlitECSService",
    cluster=cluster,
    task_definition=fargate_task_definition,
    service_name=f"{self.prefix}-stl-front",
    security_groups=[self.ecs_security_group],
    vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
    health_check_grace_period=Duration.seconds(900),
    # Temporarily disable circuit breaker
    # circuit_breaker=ecs.DeploymentCircuitBreaker(rollback=True),
)


service = ecs.FargateService(
    self,
    "StreamlitECSService",
    cluster=cluster,
    task_definition=fargate_task_definition,
    service_name=f"{self.prefix}-stl-front",
    security_groups=[self.ecs_security_group],
    vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
    health_check_grace_period=cdk.Duration.seconds(300),  # Increase to give tasks more time to become healthy
)


service = ecs.FargateService(
    self,
    "StreamlitECSService",
    cluster=cluster,
    task_definition=fargate_task_definition,
    service_name=f"{self.prefix}-stl-front",
    security_groups=[self.ecs_security_group],
    vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
    health_check_grace_period=cdk.Duration.seconds(300),  # Extends the grace period before ECS starts checking container health
    deployment_controller=ecs.DeploymentController(type=ecs.DeploymentControllerType.ECS),
    circuit_breaker=ecs.DeploymentCircuitBreaker(
        rollback=True  # Enable automatic rollback on failure
    ),
    deployment_configuration=ecs.DeploymentConfiguration(
        maximum_percent=200,  # Maximum percentage of running tasks during deployment
        minimum_healthy_percent=50  # Minimum percentage of healthy tasks during deployment
    )
)


To address the issue of CloudFormation hanging during updates or rollbacks with
your ECS service, the following settings from the previous response are particularly relevant:

1. Health Check Grace Period

Parameter:
health_check_grace_period
Purpose:
This setting allows newly launched tasks more time to initialize before ECS
starts performing health checks. If your tasks take a while to start up, increasing this 
period can prevent them from being marked unhealthy prematurely, which can cause deployments to hang.

service = ecs.FargateService(
    self,
    "StreamlitECSService",
    cluster=cluster,
    task_definition=fargate_task_definition,
    service_name=f"{self.prefix}-stl-front",
    security_groups=[self.ecs_security_group],
    vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
    health_check_grace_period=cdk.Duration.seconds(300),  # Increase to give tasks more time to become healthy
)


from aws_cdk import Duration
from aws_cdk import aws_ecs as ecs

fargate_task_definition.add_container(
    "WebContainer",
    image=ecs.ContainerImage.from_docker_image_asset(self.docker_asset),
    port_mappings=[ecs.PortMapping(container_port=8501, protocol=ecs.Protocol.TCP)],
    environment={
        "CLIENT_ID": self.client_id,
        "API_URI": self.api_uri,
        "BUCKET_NAME": self.s3_data_bucket.bucket_name,
        "COVER_IMAGE_URL": self.cover_image_url,
        "COVER_IMAGE_LOGIN_URL": self.cover_image_login_url,
        "EMAIL_ENABLED": self.email_enabled,
        "SMS_ENABLED": self.sms_enabled,
        "CUSTOM_ENABLED": self.custom_enabled
    },
    logging=ecs.LogDrivers.aws_logs(stream_prefix="WebContainerLogs"),
    health_check=ecs.HealthCheck(
        command=["CMD-SHELL", "curl -f http://localhost:8501/ || exit 1"],
        interval=Duration.seconds(60),  # How often to check the container (default: 30s)
        timeout=Duration.seconds(10),   # Time to wait before considering a health check failed (default: 5s)
        retries=3,                       # Number of retries to perform (default: 3)
        start_period=Duration.seconds(120)  # Grace period after container starts before health check starts (default: 0s)
    )
)


from aws_cdk import (
    Duration,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_logs as logs,
)
from constructs import Construct

class MyEcsService(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Define ECS Task Definition and Fargate Service
        fargate_task_definition = ecs.FargateTaskDefinition(
            self, "WebappTaskDef", memory_limit_mib=512, cpu=256
        )

        fargate_task_definition.add_container(
            "WebContainer",
            image=ecs.ContainerImage.from_docker_image_asset(self.docker_asset),
            port_mappings=[ecs.PortMapping(container_port=8501, protocol=ecs.Protocol.TTCP)],
            environment={
                "CLIENT_ID": "example-client-id",
                "API_URI": "https://api.example.com",
                "BUCKET_NAME": "my-s3-bucket",
                "COVER_IMAGE_URL": "https://example.com/image.jpg",
                "COVER_IMAGE_LOGIN_URL": "https://example.com/login-image.jpg",
                "EMAIL_ENABLED": "true",
                "SMS_ENABLED": "true",
                "CUSTOM_ENABLED": "true"
            },
            logging=ecs.LogDrivers.aws_logs(stream_prefix="WebContainerLogs"),
            health_check=ecs.HealthCheck(
                command=["CMD-SHELL", "curl -f http://localhost:8501/ || exit 1"],
                interval=Duration.seconds(60),
                timeout=Duration.seconds(10),
                retries=3,
                start_period=Duration.seconds(120)
            )
        )

        service = ecs.FargateService(
            self,
            "StreamlitECSService",
            cluster=ecs.Cluster(self, "MyCluster", vpc=ec2.Vpc(self, "MyVpc")),
            task_definition=fargate_task_definition,
            service_name="stl-front",
            security_groups=[ec2.SecurityGroup(self, "MySecurityGroup", vpc=ec2.Vpc(self, "MyVpc"))],
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            health_check_grace_period=Duration.seconds(300),
        )


"""
The error you're encountering, AttributeError: module 'aws_cdk.aws_ecs' has no attribute
'DeploymentConfiguration', suggests that the DeploymentConfiguration attribute does not exist
the aws_cdk.aws_ecs module, which is likely due to a version mismatch or the class
being deprecated or removed in the AWS CDK library you are using.

Resolving the Issue:

Check CDK Version:
Ensure that your AWS CDK library is up to date. The DeploymentConfiguration might have 
been renamed or its usage could have changed in the version of the CDK you are using.
Alternative Approach:

Instead of using DeploymentConfiguration, you can set the deployment options directly
within the FargateService or Ec2Service using deployment_controller and the appropriate attributes.
Here’s how you can configure deployment options without using DeploymentConfiguration:

Updated Code Without DeploymentConfiguration:
"""


from aws_cdk import (
    Duration,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_logs as logs,
)
from constructs import Construct

class MyEcsService(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Define ECS Task Definition and Fargate Service
        fargate_task_definition = ecs.FargateTaskDefinition(
            self, "WebappTaskDef", memory_limit_mib=512, cpu=256
        )

        fargate_task_definition.add_container(
            "WebContainer",
            image=ecs.ContainerImage.from_docker_image_asset(self.docker_asset),
            port_mappings=[ecs.PortMapping(container_port=8501, protocol=ecs.Protocol.TCP)],
            environment={
                "CLIENT_ID": "example-client-id",
                "API_URI": "https://api.example.com",
                "BUCKET_NAME": "my-s3-bucket",
                "COVER_IMAGE_URL": "https://example.com/image.jpg",
                "COVER_IMAGE_LOGIN_URL": "https://example.com/login-image.jpg",
                "EMAIL_ENABLED": "true",
                "SMS_ENABLED": "true",
                "CUSTOM_ENABLED": "true"
            },
            logging=ecs.LogDrivers.aws_logs(stream_prefix="WebContainerLogs"),
            health_check=ecs.HealthCheck(
                command=["CMD-SHELL", "curl -f http://localhost:8501/ || exit 1"],
                interval=Duration.seconds(60),
                timeout=Duration.seconds(10),
                retries=3,
                start_period=Duration.seconds(120)
            )
        )

        service = ecs.FargateService(
            self,
            "StreamlitECSService",
            cluster=ecs.Cluster(self, "MyCluster", vpc=ec2.Vpc(self, "MyVpc")),
            task_definition=fargate_task_definition,
            service_name="stl-front",
            security_groups=[ec2.SecurityGroup(self, "MySecurityGroup", vpc=ec2.Vpc(self, "MyVpc"))],
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            health_check_grace_period=Duration.seconds(300),
            circuit_breaker=ecs.DeploymentCircuitBreaker(rollback=True),  # Enable rollback on failure
            deployment_controller=ecs.DeploymentController(type=ecs.DeploymentControllerType.ECS),  # Set deployment type
        )

"""
Key Changes:
Removed DeploymentConfiguration: This class does not exist, so it's not used.
Used circuit_breaker and deployment_controller: These are valid settings for
controlling how deployments behave in the absence of DeploymentConfiguration.

Recommendations:

Update CDK:
Always check if you're using the latest version of CDK, as API changes
can occur between versions.

Review Documentation:
If you're unsure about certain attributes or classes, checking
the AWS CDK documentation for your specific version can provide clarity.
This should help resolve the issue and enable you to manage your ECS deployments
without encountering the AttributeError

The error message indicates that the ECS Deployment Circuit Breaker was triggered
again, which typically means that the ECS service deployment failed, likely due to the
ECS tasks not becoming healthy within the expected timeframe.

Potential Causes and Solutions

Health Check Failures:

Check Logs:
Ensure that the ECS tasks are able to start correctly and pass the health
checks. Look at the ECS service and task logs in CloudWatch to diagnose why the health
checks might be failing.

Adjust Health Check Settings:
If your application takes a long time to start, consider
increasing the start_period in the health check configuration, which is the period before
the health checks start running after a task is launched.
"""


fargate_task_definition.add_container(
    "WebContainer",
    image=ecs.ContainerImage.from_docker_image_asset(self.docker_asset),
    port_mappings=[ecs.PortMapping(container_port=8501, protocol=ecs.Protocol.TCP)],
    environment={
        "CLIENT_ID": self.client_id,
        "API_URI": self.api_uri,
        "BUCKET_NAME": self.s3_data_bucket.bucket_name,
        "COVER_IMAGE_URL": self.cover_image_url,
        "COVER_IMAGE_LOGIN_URL": self.cover_image_login_url,
        "EMAIL_ENABLED": self.email_enabled,
        "SMS_ENABLED": self.sms_enabled,
        "CUSTOM_ENABLED": self.custom_enabled
    },
    logging=ecs.LogDrivers.aws_logs(stream_prefix="WebContainerLogs"),
    health_check=ecs.HealthCheck(
        command=["CMD-SHELL", "curl -f http://localhost:8501/ || exit 1"],
        interval=Duration.seconds(60),
        timeout=Duration.seconds(10),
        retries=3,
        start_period=Duration.seconds(300)  # Increase to 5 minutes if necessary
    )
)


service = ecs.FargateService(
    self,
    "StreamlitECSService",
    cluster=cluster,
    task_definition=fargate_task_definition,
    service_name=f"{self.prefix}-stl-front",
    security_groups=[self.ecs_security_group],
    vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
    # Increase to give tasks more time to become healthy
    health_check_grace_period=cdk.Duration.seconds(300), 
)


2. Circuit Breaker
Parameter:
circuit_breaker
Purpose:
Enabling the circuit breaker allows the service to automatically roll back
to the last known stable state if the deployment fails. This prevents a failed update
from leaving the service in a "hanging" state.


service = ecs.FargateService(
    self,
    "StreamlitECSService",
    cluster=cluster,
    task_definition=fargate_task_definition,
    service_name=f"{self.prefix}-stl-front",
    security_groups=[self.ecs_security_group],
    vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
    circuit_breaker=ecs.DeploymentCircuitBreaker(
        rollback=True  # Automatically rollback on failure
    ),
)


3. Deployment Configuration
Parameter:
deployment_configuration
Purpose:
Adjusting the maximum_percent and minimum_healthy_percent allows you
to control how many tasks can be replaced during an update. For instance, setting
a higher maximum_percent or a lower minimum_ healthy_percent can make updates
less aggressive and provide more room for tasks to start successfully.


service = ecs.FargateService(
    self,
    "StreamlitECSService",
    cluster=cluster,
    task_definition=fargate_task_definition,
    service_name=f"{self.prefix}-stl-front",
    security_groups=[self.ecs_security_group],
    vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
    deployment_configuration=ecs.DeploymentConfiguration(
        maximum_percent=200,  # Allow more tasks to run during an update
        minimum_healthy_percent=50  # Require fewer healthy tasks during deployment
    ),
)


1. Increase Health Check Timeout
You can configure the health check for your container and set the timeout value, 
which is the amount of time to wait before deciding that a health check has failed.

fargate_task_definition.add_container(
    "WebContainer",
    image=ecs.ContainerImage.from_docker_image_asset(self.docker_asset),
    port_mappings=[ecs.PortMapping(container_port=8501, protocol=ecs.Protocol.TCP)],
    environment={
        "CLIENT_ID": self.client_id,
        "API_URI": self.api_uri,
        "BUCKET_NAME": self.s3_data_bucket.bucket_name,
        "COVER_IMAGE_URL": self.cover_image_url,
        "COVER_IMAGE_LOGIN_URL": self.cover_image_login_url,
        "EMAIL_ENABLED": self.email_enabled,
        "SMS_ENABLED": self.sms_enabled,
        "CUSTOM_ENABLED": self.custom_enabled
    },
    logging=ecs.LogDrivers.aws_logs(stream_prefix="WebContainerLogs"),
    health_check=ecs.HealthCheck(
        command=["CMD-SHELL", "curl -f http://localhost:8501/ || exit 1"],
        interval=cdk.Duration.seconds(60),  # How often to check the container (default: 30s)
        timeout=cdk.Duration.seconds(10),   # Time to wait before considering a health check failed (default: 5s)
        retries=3,                          # Number of retries to perform (default: 3)
        start_period=cdk.Duration.seconds(120)  # Grace period after container starts before health check starts (default: 0s)
    )
)


2. Increase ECS Service Deployment Timeouts

You can also adjust the deployment circuit breaker and deployment configuration in
the FargateService definition to manage how the service handles deployment failures
and to extend the time the service waits during a deployment.

Explanation:

Health Check Timeout:
The health_check block allows you to specify how often and
with what timeout a health check should be performed.

Health Check Grace Period:
Extends the grace period before ECS starts health checks
on the new task. This is particularly useful if your application takes longer to start.

Circuit Breaker:
Automatically rolls back the service to a previous healthy state if the deployment fails.

Deployment Configuration:
Adjusts how aggressively the service is updated (i.e., how many
tasks are taken down or started simultaneously during an update).
By increasing these timeouts and settings, you give your ECS tasks more time
to start up and stabilize before they are deemed unhealthy or before an update fails.
This can help prevent your CloudFormation stack from hanging during updates.


service = ecs.FargateService(
    self,
    "StreamlitECSService",
    cluster=cluster,
    task_definition=fargate_task_definition,
    service_name=f"{self.prefix}-stl-front",
    security_groups=[self.ecs_security_group],
    vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
    health_check_grace_period=cdk.Duration.seconds(300),  # Extends the grace period before ECS starts checking container health
    deployment_controller=ecs.DeploymentController(type=ecs.DeploymentControllerType.ECS),
    circuit_breaker=ecs.DeploymentCircuitBreaker(
        rollback=True  # Enable automatic rollback on failure
    ),
    deployment_configuration=ecs.DeploymentConfiguration(
        maximum_percent=200,  # Maximum percentage of running tasks during deployment
        minimum_healthy_percent=50  # Minimum percentage of healthy tasks during deployment
    )
)


To set the desired number of tasks in an AWS Fargate service using AWS CDK,
you need to specify the desired_count property when defining the FargateService.
This property determines the number of tasks that the service should maintain.

Example of Setting Desired Tasks in Fargate Service
Here’s how you can set the desired count of tasks in your Fargate service using AWS CDK:


from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_logs as logs,
    Duration
)
from constructs import Construct

class MyEcsService(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Define ECS Cluster
        cluster = ecs.Cluster(self, "MyCluster", vpc=ec2.Vpc(self, "MyVpc"))

        # Define Fargate Task Definition
        fargate_task_definition = ecs.FargateTaskDefinition(
            self, "WebappTaskDef", memory_limit_mib=512, cpu=256
        )

        fargate_task_definition.add_container(
            "WebContainer",
            image=ecs.ContainerImage.from_docker_image_asset(self.docker_asset),
            port_mappings=[ecs.PortMapping(container_port=8501, protocol=ecs.Protocol.TCP)],
            logging=ecs.LogDrivers.aws_logs(stream_prefix="WebContainerLogs"),
            environment={
                "CLIENT_ID": "example-client-id",
                "API_URI": "https://api.example.com",
                "BUCKET_NAME": "my-s3-bucket"
            },
            health_check=ecs.HealthCheck(
                command=["CMD-SHELL", "curl -f http://localhost:8501/ || exit 1"],
                interval=Duration.seconds(60),
                timeout=Duration.seconds(10),
                retries=3,
                start_period=Duration.seconds(120)
            )
        )

        # Define Fargate Service with desired task count
        service = ecs.FargateService(
            self,
            "StreamlitECSService",
            cluster=cluster,
            task_definition=fargate_task_definition,
            desired_count=3,  # Set the desired number of tasks
            service_name="stl-front",
            security_groups=[ec2.SecurityGroup(self, "MySecurityGroup", vpc=ec2.Vpc(self, "MyVpc"))],
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            health_check_grace_period=Duration.seconds(300),
        )


Explanation:

desired_count:
This property sets the desired number of tasks that should be running
for this service. In the example above, desired_count=3 means the service will always
attempt to maintain three running tasks.

Task Definition:
The fargate_task_definition is where you define the container
configurations, such as image, environment variables, and health checks.  Cluster
and Service: The service is deployed to an ECS cluster, and the security groups and
subnets define the networking configuration.

Use Cases:

Auto Scaling:
If you want to enable auto-scaling, you can start with a desired_count and then attach an auto-scaling policy to adjust the number of tasks based on metrics like CPU utilization or custom CloudWatch metrics.

Adding Auto-Scaling:
If you want to add auto-scaling to your Fargate service, you can do so like this:


scalable_target = service.auto_scale_task_count(
    min_capacity=1,
    max_capacity=10
)

scalable_target.scale_on_cpu_utilization("CpuScaling", target_utilization_percent=50)