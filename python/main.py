import json

import ee
import eeconvert
import geopandas as gpd
import typer
from matplotlib import pyplot as plt
from planet_emu.earth_engine.enum import ImageCollectionEnum, ImageEnum
from shapely import geometry

app = typer.Typer()


@app.command()
def image_collection(
    enum: ImageCollectionEnum = ImageCollectionEnum.WEATHER, stats: bool = False
):
    typer.echo("Image collection: {}".format(enum.name))

    image_collection = ee.ImageCollection(enum.name)

    if stats:
        rectangle = geometry.box(-90, 30, -89, 31)
        input_gdf = gpd.GeoDataFrame(geometry=[rectangle], crs="EPSG:4326")  # type: ignore
        input_fc = eeconvert.gdfToFc(input_gdf)

        image: ee.Image = image_collection.filterDate("2020-01-01", "2020-02-01").mean()
        output_fc = image.reduceRegions(
            input_fc,
            reducer=ee.Reducer.mean(),
            scale=enum.scale,
            crs="EPSG:4326",
            tileScale=1,
        )
        output_gdf = eeconvert.fcToGdf(output_fc)
        output_gdf.to_csv("../data/cli.csv")

        typer.echo("Plotting")

        output_gdf.plot(column=output_gdf.columns[0], cmap="viridis", legend=True)
        plt.savefig(
            "../images/cli.png",
            dpi=1000,
        )
    else:
        first_image: dict = (
            image_collection.sort("system:time_start", True).first().getInfo()
        )
        last_image: dict = (
            image_collection.sort("system:time_start", False).first().getInfo()
        )
        image_count: int = image_collection.size().getInfo()  # type: ignore

        typer.echo("First image: {}".format(first_image.get("id")))
        typer.echo("Last image: {}".format(last_image.get("id")))
        typer.echo("Image count: {}".format(image_count))


@app.command()
def image(enum: ImageEnum = ImageEnum.BULK_DENSITY):
    typer.echo("Image: {}".format(enum.name))

    image = ee.Image(enum.name)

    typer.echo(json.dumps(image.getInfo(), indent=4))


if __name__ == "__main__":
    app()
