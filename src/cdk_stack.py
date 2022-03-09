import aws_cdk as core
from aws_cdk import aws_lambda as lambda_
from constructs import Construct

class ExecutionStack(core.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        genesis_point_function = lambda_.Function(
            self, "genesis-point-function",
            function_name="genesis-point",
        )
