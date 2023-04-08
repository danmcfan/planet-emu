import os

import geopandas as gpd
import pandas as pd
import tensorflow as tf
import typer
from planet_emu.earth_engine.enum import ImageEnum
from planet_emu.earth_engine.fetch import fetch_ndvi, fetch_soil, fetch_weather
from planet_emu.grid import divide_polygon
from planet_emu.learn import create_sequential_model, load_data
from planet_emu.polygon import create_polygon
from planet_emu.predict import Features, predict_features

app = typer.Typer()


@app.command()
def ingest(
    state_name: str = "california",
    scale: int = 1000,
    output_folder: str | None = None,
):
    if output_folder is None:
        output_folder = get_output_folder(state_name, scale)

    typer.echo(f"Creating polygon grid for '{state_name}'...")
    polygon = create_polygon(state_name)
    grid_gdf = divide_polygon(polygon, scale)
    typer.echo(f"Grid size: {len(grid_gdf)}")

    for member in ImageEnum:
        typer.echo(f"Fetching {member.value} data...")
        soil_gdf = fetch_soil(grid_gdf, member, scale)
        save_csv(soil_gdf, output_folder, member.value)

    typer.echo("Fetching weather data...")
    weather_gdf = fetch_weather(grid_gdf, scale)
    save_csv(weather_gdf, output_folder, "weather")

    typer.echo("Fetching NDVI data...")
    ndvi_gdf = fetch_ndvi(grid_gdf, scale)
    save_csv(ndvi_gdf, output_folder, "ndvi")


@app.command()
def combine(
    state_name: str = "california",
    scale: int = 1000,
    output_folder: str | None = None,
):
    if output_folder is None:
        output_folder = get_output_folder(state_name, scale)

    final_df = None

    typer.echo("Combining CSVs...")
    for property in (
        "bulk_density",
        "clay",
        "organic_carbon",
        "ph",
        "sand",
        "water_content",
        "weather",
        "ndvi",
    ):
        input_filepath = os.path.join(output_folder, f"{property}.csv")
        df = pd.read_csv(input_filepath, index_col=0)

        if final_df is None:
            final_df = df
        else:
            final_df = final_df.join(df)

    for col in (
        "bulk_density_b0",
        "clay_b0",
        "organic_carbon_b0",
        "ph_b0",
        "sand_b0",
        "water_content_b0",
        "prcp",
        "ndvi",
    ):
        final_df = final_df[~final_df[col].isna()]

    typer.echo("Saving final CSV...")
    output_filepath = os.path.join(output_folder, "final.csv")
    final_df.to_csv(output_filepath, index=True)


@app.command()
def train(
    state_name: str = "california",
    scale: int = 1000,
    output_folder: str | None = None,
    epochs: int = 100,
    batch_size: int = 10_000,
    verbose: int = 2,
    create: bool = False,
):
    if output_folder is None:
        output_folder = get_output_folder(state_name, scale)

    input_filepath = os.path.join(output_folder, "final.csv")

    x_train, y_train, x_test, y_test = load_data(input_filepath)

    if create:
        model = create_sequential_model(input_size=x_train.shape[1])
    else:
        model = tf.keras.models.load_model(os.path.join(output_folder, "model"))

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss=tf.keras.losses.MeanSquaredError(),
        metrics=["mse"],
    )

    model.fit(
        x_train,
        y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(x_test, y_test),
        verbose=verbose,
    )

    model.save(os.path.join(output_folder, "model"))


@app.command()
def predict():
    features = Features(
        **{
            "bulk_density_b0": 105,
            "bulk_density_b10": 110,
            "bulk_density_b30": 130,
            "bulk_density_b60": 130,
            "bulk_density_b100": 120,
            "bulk_density_b200": 125,
            "clay_b0": 25,
            "clay_b10": 25,
            "clay_b30": 30,
            "clay_b60": 25,
            "clay_b100": 25,
            "clay_b200": 25,
            "ph_b0": 10,
            "ph_b10": 10,
            "ph_b30": 5,
            "ph_b60": 5,
            "ph_b100": 5,
            "ph_b200": 5,
            "sand_b0": 60,
            "sand_b10": 60,
            "sand_b30": 60,
            "sand_b60": 60,
            "sand_b100": 60,
            "sand_b200": 60,
            "organic_carbon_b0": 45,
            "organic_carbon_b10": 45,
            "organic_carbon_b30": 45,
            "organic_carbon_b60": 45,
            "organic_carbon_b100": 45,
            "organic_carbon_b200": 45,
            "water_content_b0": 35,
            "water_content_b10": 35,
            "water_content_b30": 35,
            "water_content_b60": 35,
            "water_content_b100": 35,
            "water_content_b200": 35,
            "prcp": 5,
            "srad": 300,
            "swe": 0,
            "tmax": 15,
            "tmin": 10,
            "vp": 1000,
        }
    )

    for k, v in features.dict().items():
        typer.echo(f"{k}: {v}")
        typer.echo(f"Type: {type(k)}")
        typer.echo(f"Type: {type(v)}")

    prediction = predict_features(features)
    typer.echo(f"Prediction: {prediction}")


def get_output_folder(state_name: str, scale: int) -> str:
    parent_folder = os.path.dirname(os.path.dirname(__file__))

    output_folder = os.path.join(parent_folder, f"data/{state_name.lower()}_{scale}")
    os.makedirs(output_folder, exist_ok=True)
    return output_folder


def save_csv(df: gpd.GeoDataFrame, output_folder: str, property: str):
    output_filepath = os.path.join(output_folder, f"{property}.csv")

    df = df.drop(columns=["geometry"])
    df.to_csv(output_filepath, index=True)


if __name__ == "__main__":
    app()
