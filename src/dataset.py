import os


from torch.utils.data import Dataset
from rasterio.merge import merge
from sklearn.preprocessing import StandardScaler
import torch
import numpy as np


class PixelDataset(Dataset):
    def __init__(self, input_dir: str):
        bands = []
        for layer in ["bulkdens", "clay", "ocarbon", "ph", "sand", "water", "daymet"]:
            src, _ = merge(
                [
                    f"{input_dir}/{layer}/{filename}"
                    for filename in os.listdir(f"{input_dir}/{layer}")
                ]
            )
            for band in src:
                band = band.flatten()
                bands.append(band)

        features = np.stack(bands, axis=-1)

        self.scaler = StandardScaler()
        features_normalized = self.scaler.fit_transform(features)

        self.features = torch.tensor(features_normalized, dtype=torch.float32)

        src, _ = merge(
            [
                f"{input_dir}/landsat/{filename}"
                for filename in os.listdir(f"{input_dir}/landsat")
            ]
        )
        self.ndvi = torch.tensor(src.flatten(), dtype=torch.float32)

    def __len__(self):
        return self.features.shape[0]

    def __getitem__(self, idx):
        return self.features[idx], torch.tensor([self.ndvi[idx]], dtype=torch.float32)
