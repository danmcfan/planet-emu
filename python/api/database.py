import boto3
import schemas

dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
table = dynamodb.Table("ndvi-prediction-tasks")


def create_task(
    id: str,
    status: schemas.Status,
    features: schemas.Features,
    prediction: float | None = None,
) -> schemas.Task:
    task = schemas.Task(id=id, status=status, features=features, prediction=prediction)

    table.put_item(Item=task.dict())

    return task


def get_task(id: str) -> schemas.Task | None:
    item = table.get_item(Key={"id": id}).get("Item")

    print(item)

    return schemas.Task(**item) if item is not None else None


def update_item(
    id: str,
    status: schemas.Status | None = None,
    features: schemas.Features | None = None,
    prediction: float | None = None,
) -> schemas.Task | None:
    task = get_task(id)

    if task is None:
        return None

    if status is not None:
        task.status = status
    if features is not None:
        task.features = features
    if prediction is not None:
        task.prediction = prediction

    table.update_item(
        Key={"id": id},
        UpdateExpression="SET status  = :s, features = :f, prediction = :p",
        ExpressionAttributeValues={
            ":s": task.status,
            ":f": task.features.dict(),
            ":p": task.prediction,
        },
    )
    return task


def delete_task(id: str) -> None:
    table.delete_item(Key={"id": id})
