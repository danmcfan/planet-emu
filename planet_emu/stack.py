import aws_cdk as cdk
from aws_cdk import aws_lambda as lambda_, aws_iam as iam, aws_apigateway as apigw
from constructs import Construct
import os


class FastAPIStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        environment = {
            "DECRYPT_PASSWORD": os.getenv("DECRYPT_PASSWORD"),
            "GCP_SERVICE_NAME": os.getenv("GCP_SERVICE_NAME"),
            "GCP_PROJECT": os.getenv("GCP_PROJECT"),
            "BUCKET": os.getenv("BUCKET"),
            "JSON_DIR": os.getenv("JSON_DIR"),
        }

        fast_api_function = lambda_.DockerImageFunction(
            self,
            "fast-api-lambda-function",
            function_name="fast-api-lambda-function",
            code=lambda_.DockerImageCode.from_image_asset(
                ".",
                cmd=["planet_emu.fast_api.main.handler"],
                build_args={"DECRYPT_PASSWORD": os.getenv("DECRYPT_PASSWORD")},
            ),
            timeout=cdk.Duration.seconds(60),
            memory_size=128,
            environment=environment,
        )

        fast_api_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "s3:*",
                    "lambda:*",
                ],
                resources=["*"],
            )
        )

        features_lambda_function = lambda_.DockerImageFunction(
            self,
            "get-point-features-lambda-function",
            function_name="get-point-features",
            code=lambda_.DockerImageCode.from_image_asset(
                ".",
                cmd=["planet_emu.fast_api.main.handler"],
                build_args={"DECRYPT_PASSWORD": os.getenv("DECRYPT_PASSWORD")},
            ),
            timeout=cdk.Duration.seconds(300),
            memory_size=1024,
            environment=environment,
        )

        features_lambda_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "s3:*",
                    "lambda:*",
                ],
                resources=["*"],
            )
        )

        rest_api = apigw.LambdaRestApi(
            self, "fast-api-rest-api", handler=fast_api_function
        )
