import os

import schemas
import numpy as np
import tensorflow as tf


def predict_features(features: schemas.Features) -> float:
    model = load_model()

    features = features_to_ndarray(features)

    predictions = model.predict(features)

    prediction = float(predictions[0][0])

    return prediction


def load_model() -> tf.keras.Sequential:
    current_folder = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_folder, "data/ndvi")

    return tf.keras.models.load_model(filepath)


def features_to_ndarray(features: schemas.Features) -> np.ndarray[np.ndarray]:
    keys = (
        "bulk_density_b0",
        "bulk_density_b10",
        "bulk_density_b100",
        "bulk_density_b200",
        "bulk_density_b30",
        "bulk_density_b60",
        "clay_b0",
        "clay_b10",
        "clay_b100",
        "clay_b200",
        "clay_b30",
        "clay_b60",
        "organic_carbon_b0",
        "organic_carbon_b10",
        "organic_carbon_b100",
        "organic_carbon_b200",
        "organic_carbon_b30",
        "organic_carbon_b60",
        "ph_b0",
        "ph_b10",
        "ph_b100",
        "ph_b200",
        "ph_b30",
        "ph_b60",
        "sand_b0",
        "sand_b10",
        "sand_b100",
        "sand_b200",
        "sand_b30",
        "sand_b60",
        "water_content_b0",
        "water_content_b10",
        "water_content_b100",
        "water_content_b200",
        "water_content_b30",
        "water_content_b60",
        "prcp",
        "srad",
        "swe",
        "tmax",
        "tmin",
        "vp",
    )

    normalizations = {
        "bulk_density_b0": {"max": 184.4038461538462, "min": 18.0},
        "bulk_density_b10": {"max": 184.1923076923077, "min": 22.0},
        "bulk_density_b100": {"max": 194.03846153846155, "min": 29.0},
        "bulk_density_b200": {"max": 194.03846153846155, "min": 44.0},
        "bulk_density_b30": {"max": 187.8269230769231, "min": 29.0},
        "bulk_density_b60": {"max": 192.40384615384616, "min": 29.0},
        "clay_b0": {"max": 47.78787878787879, "min": 2.0},
        "clay_b10": {"max": 48.0, "min": 2.0},
        "clay_b100": {"max": 47.78787878787879, "min": 2.208955223880597},
        "clay_b200": {"max": 45.91878172588832, "min": 2.238805970149253},
        "clay_b30": {"max": 49.0, "min": 2.0},
        "clay_b60": {"max": 48.7878787878788, "min": 2.055555555555556},
        "organic_carbon_b0": {"max": 52.364532019704434, "min": 0.0},
        "organic_carbon_b10": {"max": 52.15270935960592, "min": 0.0},
        "organic_carbon_b100": {"max": 63.27317073170733, "min": 0.0},
        "organic_carbon_b200": {"max": 61.009756097560974, "min": 0.0},
        "organic_carbon_b30": {"max": 69.73170731707319, "min": 0.0},
        "organic_carbon_b60": {"max": 69.61951219512194, "min": 0.0},
        "ph_b0": {"max": 86.0, "min": 45.23076923076923},
        "ph_b10": {"max": 86.0, "min": 45.44102564102565},
        "ph_b100": {"max": 90.0, "min": 47.20918367346938},
        "ph_b200": {"max": 90.0, "min": 48.0},
        "ph_b30": {"max": 88.0, "min": 46.20918367346939},
        "ph_b60": {"max": 89.0, "min": 46.21025641025641},
        "prcp": {"max": 7.406788713504106, "min": 0.1416568263780837},
        "sand_b0": {"max": 84.7309644670051, "min": 11.443877551020408},
        "sand_b10": {"max": 85.57635467980295, "min": 11.443877551020408},
        "sand_b100": {"max": 86.57635467980295, "min": 12.888324873096446},
        "sand_b200": {"max": 88.0, "min": 14.081218274111675},
        "sand_b30": {"max": 84.74619289340102, "min": 11.443877551020408},
        "sand_b60": {"max": 85.78817733990148, "min": 11.443877551020408},
        "srad": {"max": 579.1976190476191, "min": 208.6491017659505},
        "swe": {"max": 1506.1776380351946, "min": 0.0},
        "tmax": {"max": 32.92632858425964, "min": 0.3468545377254486},
        "tmin": {"max": 17.11409880980006, "min": -10.810176982215388},
        "vp": {"max": 1274.3036358613922, "min": 206.1700100115876},
        "water_content_b0": {"max": 62.0, "min": 1.0},
        "water_content_b10": {"max": 63.0, "min": 1.0},
        "water_content_b100": {"max": 59.0, "min": 1.191588785046729},
        "water_content_b200": {"max": 54.72251308900524, "min": 1.2065727699530515},
        "water_content_b30": {"max": 61.0, "min": 1.0},
        "water_content_b60": {"max": 59.0, "min": 1.2102803738317756},
    }

    features = features.dict()

    values = []
    for key in features:
        value = float(features[key])
        min = normalizations[key]["min"]
        max = normalizations[key]["max"]

        if value < min:
            values.append(0.0)
        elif value > max:
            values.append(1.0)
        else:
            values.append((value - min) / (max - min))

    return np.array([np.array(values, dtype=np.float32)])
