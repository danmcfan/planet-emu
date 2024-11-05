import os
import logging

import click
import torch
import torch.nn as nn
import torch.optim as optim

from torch.utils.data import DataLoader, random_split

from src.dataset import PixelDataset
from src.model import NDVIPredictionModel, train_model, evaluate_model

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--input_dir", default="data", help="Input directory for model training data"
)
@click.option(
    "--output_path", default="models/ndvi.pth", help="Output filepath for trained model"
)
@click.option("--epochs", default=10, help="Number of epochs to run for training")
@click.option(
    "--split", default=0.8, help="Percentage split for training and test datasets"
)
@click.option("--batch_size", default=2048, help="Batch size for dataset iteration")
@click.option(
    "--learning_rate", default=0.001, help="Learning rate for training the model"
)
@click.option(
    "--weight_decay", default=1e-5, help="Weight decay for training the model"
)
@click.option(
    "--device", default="cuda", help="Device to use for model training and evaluation"
)
@click.option(
    "--manual_seed", default=42, help="Manual seed for generating random numbers"
)
def main(
    input_dir: str,
    output_path: str,
    epochs: int,
    split: float,
    batch_size: int,
    learning_rate: float,
    weight_decay: float,
    device: str,
    manual_seed: int,
):
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if device == "cuda" and torch.cuda.is_available():
        device = torch.device("cuda")
    elif device == "mps" and torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

    logger.info(f"Running on device: {device}")

    torch.manual_seed(manual_seed)
    full_dataset = PixelDataset(input_dir)

    train_size = int(split * len(full_dataset))
    test_size = len(full_dataset) - train_size
    train_dataset, test_dataset = random_split(full_dataset, [train_size, test_size])

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    model = NDVIPredictionModel(full_dataset.features.shape[1])
    criterion = nn.MSELoss()
    optimizer = optim.Adam(
        model.parameters(), lr=learning_rate, weight_decay=weight_decay
    )

    logger.info("Starting model training...")
    train_model(model, train_loader, criterion, optimizer, epochs, device)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    torch.save(model.state_dict(), output_path)

    logger.info("Training completed and model saved.")

    logger.info("Evaluating model on test set:")
    evaluate_model(model, test_loader, criterion, device)

    model.eval()
    with torch.no_grad():
        sample_input = full_dataset.features[0].unsqueeze(0).to(device)
        predicted_ndvi = model(sample_input)
        logger.info(f"Sample prediction:")
        logger.info(f"Sample input values: {sample_input}")
        logger.info(f"Predicted NDVI: {predicted_ndvi.item():.4f}")
        logger.info(f"Actual NDVI: {full_dataset.ndvi[0].item():.4f}")


if __name__ == "__main__":
    main()
