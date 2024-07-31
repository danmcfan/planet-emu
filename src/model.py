import time
import logging

import numpy as np
import torch
import torch.nn as nn

logger = logging.getLogger(__name__)


class NDVIPredictionModel(nn.Module):
    def __init__(self, input_size: int):
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
        epoch_start_time = time.perf_counter()

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
        epoch_elapsed_time = time.perf_counter() - epoch_start_time
        logger.info(
            f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss}, Time: {epoch_elapsed_time:.2f}s"
        )


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

    logger.info(f"Test Loss: {avg_loss:.4f}")
    logger.info(f"MSE: {mse:.4f}")
    logger.info(f"RMSE: {rmse:.4f}")
    logger.info(f"R-squared: {r2:.4f}")
