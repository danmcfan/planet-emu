from decimal import Decimal

import database, schemas, predict


def handler(event, _) -> None:
    id = event["id"]

    try:
        task = database.get_task(id)

        prediction = predict.predict_features(task.features)

        database.update_task(
            id, status=schemas.Status.SUCCESS, prediction=Decimal(prediction)
        )
    except Exception as e:
        database.update_task(id, status=schemas.Status.FAILURE)
        raise e
