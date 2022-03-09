import aws_cdk as core
from aws_cdk import aws_lambda as lambda_, aws_iam as iam
from constructs import Construct


class ExecutionStack(core.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        function = lambda_.Function(
            self,
            "function",
            function_name="function-name",
            runtime=lambda_.Runtime.PYTHON_3_7,
            handler="main.handler",
            code=lambda_.Code.from_asset("src"),
            timeout=core.Duration.seconds(60),
            memory_size=128,
        )

        function.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("FullS3Access")
        )
