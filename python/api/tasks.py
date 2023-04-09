import json
import uuid
from typing import Any, Hashable

import boto3
import database
import schemas

lambda_client = boto3.client("lambda", region_name="us-east-2")


def invoke_prediction_lambda(features: schemas.Features) -> schemas.Task:
    id = uuid.uuid4().hex

    task = database.create_task(id, schemas.Status.PENDING, features)
    invoke_lambda("ndvi-prediction", {"id": task.id})

    return task


def invoke_lambda(function_name: str, payload: dict[Hashable, Any]) -> None:
    lambda_client.invoke(
        FunctionName=function_name,
        InvocationType="Event",
        Payload=json.dumps(payload, default=str),
    )
