from typing import Any

import pandas as pd
import tensorflow as tf


def create_sequential_model(
    input_size: int, first_layer_node_count: int = 1024, dropout_rate: float = 0.2
) -> tf.keras.Sequential:
    second_layer_node_count = first_layer_node_count // 2
    third_layer_node_count = second_layer_node_count // 2

    layers = [
        tf.keras.layers.Dense(
            first_layer_node_count, activation="relu", input_shape=(input_size,)
        ),
        tf.keras.layers.Dropout(dropout_rate),
        tf.keras.layers.Dense(second_layer_node_count, activation="relu"),
        tf.keras.layers.Dropout(dropout_rate),
        tf.keras.layers.Dense(third_layer_node_count, activation="relu"),
        tf.keras.layers.Dense(1, activation="linear"),
    ]
    return tf.keras.Sequential(layers)


def load_data(filepath: str) -> tuple[Any, Any, Any, Any]:
    dataframe = pd.read_csv(filepath)
    dataframe = dataframe.sample(frac=1)

    return split_dataset(dataframe)


def split_dataset(
    dataset: pd.DataFrame, y_col: str = "ndvi", split: float = "0.8"
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
