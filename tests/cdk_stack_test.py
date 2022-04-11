import aws_cdk as core
import aws_cdk.assertions as assertions

from planet_emu.cdk_stack import ExecutionStack


def test_lambda_function_created():
    app = core.App()
    stack = ExecutionStack(app, "cdk")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "FunctionName": "function-name",
        },
    )
