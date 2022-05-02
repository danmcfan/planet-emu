import os

import aws_cdk as cdk

from planet_emu.fast_api.stack import FastAPIStack


app = cdk.App()
execution_stack = FastAPIStack(
    app,
    "fast-api-stack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION"),
    ),
)

app.synth()
