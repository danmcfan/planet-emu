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

        lambda_function = lambda_.DockerImageFunction(
            self,
            "fast-api-lambda-function",
            function_name="fast-api-lambda-function",
            code=lambda_.DockerImageCode.from_image_asset("."),
            timeout=cdk.Duration.seconds(60),
            memory_size=128,
            environment=environment,
        )

        lambda_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "s3:*",
                    "lambda:*",
                ],
                resources=["*"],
            )
        )

        rest_api = apigw.LambdaRestApi(
            self, "fast-api-rest-api", handler=lambda_function
        )
