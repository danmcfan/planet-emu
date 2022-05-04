from typing import Any
import tensorflow as tf
from tensorflow.keras import layers
import pandas as pd


def split_dataset(
    dataset: pd.DataFrame, frac: float = 0.8
) -> tuple[pd.DataFrame, pd.DataFrame]:
    train_dataset = dataset.sample(frac=0.8, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)
    return train_dataset, test_dataset


def split_features(dataset: pd.DataFrame, y_col: str) -> tuple[pd.DataFrame, pd.Series]:
    features = dataset.copy()
    labels = features.pop(y_col)
    return features, labels


def load_model(path: str) -> Any:
    return tf.keras.models.load_model(path)


def get_model(
    train_features: pd.DataFrame,
    train_labels: pd.Series,
    learning_rate: float = 0.001,
    loss: str = "mean_absolute_percentage_error",
    epochs: int = 100,
    validation_split: float = 0.2,
) -> Any:
    normalizer = layers.Normalization()
    normalizer.adapt(train_features)

    model = tf.keras.Sequential(
        [
            normalizer,
            layers.Dense(64, activation="relu"),
            layers.Dense(64, activation="relu"),
            layers.Dense(1),
        ]
    )

    model.compile(
        optimizer=tf.optimizers.Adam(learning_rate=learning_rate),
        loss=loss,
    )

    history = model.fit(
        train_features,
        train_labels,
        epochs=epochs,
        verbose=0,
        validation_split=validation_split,
    )

    hist = pd.DataFrame(history.history)
    hist["epoch"] = history.epoch

    return model, hist


def get_evaluation(
    model: Any, test_features: pd.DataFrame, test_labels: pd.Series
) -> Any:
    return model.evaluate(test_features, test_labels, verbose=0)
