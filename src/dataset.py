import os
import logging

from torch.utils.data import Dataset
from sklearn.preprocessing import StandardScaler
import torch
import numpy as np

logger = logging.getLogger(__name__)


class PixelDataset(Dataset):
    def __init__(self, input_dir: str):
        features = []
        for layer, fields in [
            ("bulkdens", ["b0", "b10", "b30", "b60", "b100", "b200"]),
            ("clay", ["b0", "b10", "b30", "b60", "b100", "b200"]),
            ("ocarbon", ["b0", "b10", "b30", "b60", "b100", "b200"]),
            ("ph", ["b0", "b10", "b30", "b60", "b100", "b200"]),
            ("sand", ["b0", "b10", "b30", "b60", "b100", "b200"]),
            ("water", ["b0", "b10", "b30", "b60", "b100", "b200"]),
            ("daymet", ["dayl", "prcp", "srad", "swe", "tmax", "tmin", "vp"]),
        ]:
            logger.info(f"Loading {layer} files...")
            arrays = []

            for filepath in sorted(
                [
                    f"{input_dir}/{layer}/{filename}"
                    for filename in os.listdir(f"{input_dir}/{layer}")
                ]
            ):
                array: np.ndarray = np.load(filepath)
                array = np.stack([array[field] for field in fields], axis=-1)
                arrays.append(array)

            merged_array = np.stack(arrays, axis=0)
            features.append(merged_array)

        features = np.concatenate(features, axis=-1)
        features = features.reshape(-1, features.shape[-1])

        scaler = StandardScaler()
        features_normalized = scaler.fit_transform(features)

        self.features = torch.tensor(features_normalized, dtype=torch.float32)

        logger.info("Loading landsat files...")
        arrays = []
        for filepath in sorted(
            [
                f"{input_dir}/landsat/{filename}"
                for filename in os.listdir(f"{input_dir}/landsat")
            ]
        ):
            array: np.ndarray = np.load(filepath)
            array = np.stack([array[field] for field in ["SR_B5"]], axis=-1)
            arrays.append(array)

        ndvi = np.stack(arrays, axis=0)
        ndvi = ndvi.reshape(-1, ndvi.shape[-1])

        self.ndvi = torch.tensor(ndvi, dtype=torch.float32)

    def __len__(self):
        return self.features.shape[0]

    def __getitem__(self, idx):
        return self.features[idx], torch.tensor([self.ndvi[idx]], dtype=torch.float32)
