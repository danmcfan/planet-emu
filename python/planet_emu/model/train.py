import os
from typing import Any

import numpy as np
import pandas as pd
import tensorflow as tf


def create_model(input_size: int) -> tf.keras.Sequential:
    layers = [
        tf.keras.layers.Dense(32, activation="relu", input_shape=(input_size,)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(8, activation="relu"),
        tf.keras.layers.Dense(1, activation="linear"),
    ]
    model = tf.keras.Sequential(layers)

    return model


def train(
    model: tf.keras.Sequential,
    dataset: pd.DataFrame,
    y_col: str = "ndvi",
    split: float = 0.8,
    learning_rate: float = 0.001,
    epochs: int = 100,
    batch_size: int = 32,
    verbose: int = 1,
    model_name: str = "ndvi_model",
) -> tuple[tf.keras.Sequential, float, float]:
    x_train, y_train, _, _ = split_dataset(dataset, y_col, split)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss=tf.keras.losses.MeanSquaredError(),
        metrics=["mse"],
    )
    model.fit(
        x_train,
        y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=(1 - split),
        verbose=verbose,
    )

    model.save(os.path.join(os.path.dirname(__file__), model_name))
    return model


def split_dataset(
    dataset: pd.DataFrame, y_col: str, split: float
) -> tuple[Any, Any, Any, Any]:
    features, labels = split_features(dataset, y_col)
    train_size = int(len(features) * split)

    x_train = features[:train_size]
    y_train = labels[:train_size]

    x_test = features[train_size:]
    y_test = labels[train_size:]

    return x_train, y_train, x_test, y_test


def split_features(dataset: pd.DataFrame, y_col: str) -> tuple[Any, Any]:
    labels = dataset.pop(y_col)
    dataset = (dataset - dataset.min()) / (dataset.max() - dataset.min())
    features = dataset.to_numpy()

    return features, labels


def load_model(filepath: str) -> tf.keras.Sequential:
    model = tf.keras.models.load_model(filepath)
    return model
