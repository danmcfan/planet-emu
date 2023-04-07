from typing import Any

import pandas as pd
import tensorflow as tf


def load_model(path: str) -> Any:
    return tf.keras.models.load_model(path)


def predict(model: Any, features: pd.DataFrame) -> Any:
    return model.predict(features)
