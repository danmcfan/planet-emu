import os

import numpy as np
import tensorflow as tf
from planet_emu.api.schemas import Features


def predict_features(features: Features) -> float:
    model = load_model()

    predictions = model.predict(np.array([features.to_ndarray()]))
    prediction = float(predictions[0][0])

    return prediction


def load_model() -> tf.keras.Sequential:
    current_folder = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_folder, "data/model")

    return tf.keras.models.load_model(filepath)
