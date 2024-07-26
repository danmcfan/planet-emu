import json
from collections import defaultdict

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset, random_split
from sklearn.preprocessing import StandardScaler
import numpy as np


class GeojsonDataset(Dataset):
    def __init__(self, file_paths: list[str], property_mapping: dict[str, list[str]]):
        self.data = defaultdict(dict)
        self.feature_names = []
        self.property_mapping = property_mapping

        # Load data from GeoJSON files
        for file_path in file_paths:
            with open(file_path, "r") as f:
                geojson_data = json.load(f)

            file_key = file_path.split("/")[-1].split(".")[
                0
            ]  # Extract file key from filename
            properties_to_extract = self.property_mapping[file_key]
            feature_names = [
                f"{file_key}_{prop_name}" for prop_name in properties_to_extract
            ]
            self.feature_names.extend(feature_names)

            for feature in geojson_data["features"]:
                properties = feature["properties"]
                id_ = properties["id"]

                for prop_name, feature_name in zip(
                    properties_to_extract, feature_names
                ):
                    value = properties.get(prop_name, None)
                    if value is not None:
                        self.data[id_][feature_name] = value

        # Convert data to tensors
        self.ids = sorted(self.data.keys())
        features = []
        ndvi = []

        ndvi_key = f"{file_paths[-1].split('/')[-1].split('.')[0]}_{property_mapping[file_paths[-1].split('/')[-1].split('.')[0]][0]}"

        for id_ in self.ids:
            feature_values = [
                self.data[id_].get(name, 0)
                for name in self.feature_names
                if name != ndvi_key
            ]
            features.append(feature_values)
            ndvi.append([self.data[id_].get(ndvi_key, 0)])

        self.scaler = StandardScaler()
        features_normalized = self.scaler.fit_transform(features)

        self.features = torch.tensor(features_normalized, dtype=torch.float32)
        self.ndvi = torch.tensor(ndvi, dtype=torch.float32)

        print(f"Number of features: {len(self.feature_names) - 1}")
        print(f"Feature shape: {self.features.shape}")
        print(f"NDVI shape: {self.ndvi.shape}")

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, idx):
        return self.features[idx], self.ndvi[idx]


class NDVIPredictionModel(nn.Module):
    def __init__(self, input_size):
        super(NDVIPredictionModel, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 1),
        )

    def forward(self, x):
        return self.layers(x)


def train_model(model, train_loader, criterion, optimizer, num_epochs, device):
    model.to(device)
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        epoch_loss = running_loss / len(train_loader)
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss}")


def evaluate_model(model, test_loader, criterion, device):
    model.eval()
    total_loss = 0.0
    all_predictions = []
    all_targets = []

    with torch.no_grad():
        for inputs, targets in test_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            total_loss += loss.item()
            all_predictions.extend(outputs.cpu().numpy())
            all_targets.extend(targets.cpu().numpy())

    avg_loss = total_loss / len(test_loader)
    mse = np.mean((np.array(all_predictions) - np.array(all_targets)) ** 2)
    rmse = np.sqrt(mse)
    r2 = 1 - (
        np.sum((np.array(all_targets) - np.array(all_predictions)) ** 2)
        / np.sum((np.array(all_targets) - np.mean(np.array(all_targets))) ** 2)
    )

    print(f"Test Loss: {avg_loss:.4f}")
    print(f"MSE: {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R-squared: {r2:.4f}")


if __name__ == "__main__":
    # Set random seed for reproducibility
    torch.manual_seed(42)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Define paths to GeoJSON files and their property mappings
    geojson_files = [
        "data/sample/bulkdens.geojson",
        "data/sample/clay.geojson",
        "data/sample/ocarbon.geojson",
        "data/sample/ph.geojson",
        "data/sample/sand.geojson",
        "data/sample/water.geojson",
        "data/sample/daymet.geojson",
        "data/sample/modis.geojson",
    ]

    property_mapping = {
        "bulkdens": ["b0", "b10", "b30", "b60", "b100", "b200"],
        "clay": ["b0", "b10", "b30", "b60", "b100", "b200"],
        "ocarbon": ["b0", "b10", "b30", "b60", "b100", "b200"],
        "ph": ["b0", "b10", "b30", "b60", "b100", "b200"],
        "sand": ["b0", "b10", "b30", "b60", "b100", "b200"],
        "water": ["b0", "b10", "b30", "b60", "b100", "b200"],
        "daymet": [
            "dayl_mean",
            "prcp_mean",
            "srad_mean",
            "swe_mean",
            "tmax_mean",
            "tmin_mean",
            "vp_mean",
        ],
        "modis": ["mean"],
    }

    # Create full dataset
    full_dataset = GeojsonDataset(geojson_files, property_mapping)

    # Split dataset into train and test sets
    train_size = int(0.8 * len(full_dataset))
    test_size = len(full_dataset) - train_size
    train_dataset, test_dataset = random_split(full_dataset, [train_size, test_size])

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

    input_size = len(full_dataset.feature_names) - 1
    print(f"Input size: {input_size}")
    model = NDVIPredictionModel(input_size)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)

    num_epochs = 100
    train_model(model, train_loader, criterion, optimizer, num_epochs, device)

    torch.save(model.state_dict(), "models/sample/ndvi_prediction_model.pth")

    print("Training completed and model saved.")

    print("\nEvaluating model on test set:")
    evaluate_model(model, test_loader, criterion, device)

    model.eval()
    with torch.no_grad():
        sample_input = full_dataset.features[0].unsqueeze(0).to(device)
        predicted_ndvi = model(sample_input)
        print(f"\nSample prediction:")
        print(f"Sample input features: {full_dataset.feature_names[:-1]}")
        print(f"Sample input values: {sample_input}")
        print(f"Predicted NDVI: {predicted_ndvi.item():.4f}")
        print(f"Actual NDVI: {full_dataset.ndvi[0].item():.4f}")
