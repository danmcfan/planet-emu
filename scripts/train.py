import torch
from torch.utils.data import Dataset, DataLoader, random_split
from rasterio.merge import merge
import numpy as np
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
import torch.optim as optim

GRID_COUNT = 21


class PixelDataset(Dataset):
    def __init__(self):
        self.features = None
        self.ndvi = None
        self.load_data()

    def load_data(self):
        bands = []
        for layer in ["bulkdens", "clay", "ocarbon", "ph", "sand", "water", "daymet"]:
            src, _ = merge(
                [
                    f"data/{layer}/{grid_index}.geotiff"
                    for grid_index in range(GRID_COUNT)
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
            [f"data/landsat/{grid_index}.geotiff" for grid_index in range(GRID_COUNT)]
        )
        self.ndvi = torch.tensor(src.flatten(), dtype=torch.float32)

    def __len__(self):
        return self.features.shape[0]

    def __getitem__(self, idx):
        return self.features[idx], torch.tensor([self.ndvi[idx]], dtype=torch.float32)


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


def main():
    # Set random seed for reproducibility
    torch.manual_seed(42)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Create the dataset and dataloader
    full_dataset = PixelDataset()

    train_size = int(0.8 * len(full_dataset))
    test_size = len(full_dataset) - train_size
    train_dataset, test_dataset = random_split(full_dataset, [train_size, test_size])

    train_loader = DataLoader(train_dataset, batch_size=2048, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=2048, shuffle=False)

    model = NDVIPredictionModel(full_dataset.features.shape[1])
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)

    num_epochs = 20
    train_model(model, train_loader, criterion, optimizer, num_epochs, device)

    torch.save(model.state_dict(), "models/ndvi_prediction_model.pth")

    print("Training completed and model saved.")

    print("\nEvaluating model on test set:")
    evaluate_model(model, test_loader, criterion, device)

    model.eval()
    with torch.no_grad():
        sample_input = full_dataset.features[0].unsqueeze(0).to(device)
        predicted_ndvi = model(sample_input)
        print(f"\nSample prediction:")
        print(f"Sample input values: {sample_input}")
        print(f"Predicted NDVI: {predicted_ndvi.item():.4f}")
        print(f"Actual NDVI: {full_dataset.ndvi[0].item():.4f}")


if __name__ == "__main__":
    main()
