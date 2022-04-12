import os

import aws_cdk as cdk

from planet_emu.cdk_stack import ExecutionStack


app = cdk.App()
execution_stack = ExecutionStack(
    app,
    "execution-stack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION"),
    ),
)

app.synth()
