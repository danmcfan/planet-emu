from typing import Optional
from dataclasses import dataclass
import ee
import eeconvert
import geopandas as gpd
import os

from planet_emu import gee

NAME = os.getenv("GCP_SERVICE_NAME")
PROJECT = os.getenv("GCP_PROJECT")

gee.init(NAME, PROJECT)


@dataclass
class PlanetImageCollection:
    name: str
    scale: int

    def __post_init__(self):
        self.image_collection = ee.ImageCollection(self.name)

    def list_images_info(self) -> list[dict]:
        return self.image_collection.toList(self.image_collection.size()).getInfo()

    def get_reduced_image(
        self,
        reducer: str = "mean",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> ee.Image:
        image = self.image_collection

        if start_date and end_date:
            image = self.image_collection.filterDate(start_date, end_date)

        if reducer == "mean":
            image = image.mean()
        elif reducer == "median":
            image = image.median()
        elif reducer == "mode":
            image = image.mode()
        elif reducer == "min":
            image = image.min()
        elif reducer == "max":
            image = image.max()
        elif reducer == "std":
            image = image.reduce(ee.Reducer.stdDev())
        else:
            raise ValueError(f"Reducer '{reducer}' not recognized.")

        return PlanetImage(self.name, self.scale, image)


@dataclass
class PlanetImage:
    name: str
    scale: int
    image: Optional[ee.Image] = None

    def __post_init__(self):
        if self.image is None:
            self.image = ee.Image(self.name)

    def get_image_info(self) -> dict:
        return self.image.getInfo()

    def set_ndvi(
        self, red_band: str = "sur_refl_b01", nir_band: str = "sur_refl_b02"
    ) -> None:
        self.image = self.image.normalizedDifference([nir_band, red_band]).rename(
            "ndvi"
        )

    def reduce_regions(
        self,
        in_gdf: gpd.GeoDataFrame,
        tile_scale: int = 1,
        mode: bool = False,
    ) -> gpd.GeoDataFrame:
        in_fc = eeconvert.gdfToFc(in_gdf)

        if mode:
            reducer = ee.Reducer.mode()
        else:
            reducer = ee.Reducer.mean()

        out_fc = self.image.reduceRegions(
            in_fc,
            reducer=reducer,
            scale=self.scale,
            crs="EPSG:4326",
            tileScale=tile_scale,
        )
        return eeconvert.fcToGdf(out_fc)


WEATHER_IC = PlanetImageCollection(
    "NASA/ORNL/DAYMET_V4",
    1000,
)
MODIS_IC = PlanetImageCollection(
    "MODIS/061/MOD09GQ",
    250,
)

BULKDENS_IMG = PlanetImage(
    "OpenLandMap/SOL/SOL_BULKDENS-FINEEARTH_USDA-4A1H_M/v02",
    250,
)
CLAY_IMG = PlanetImage(
    "OpenLandMap/SOL/SOL_CLAY-WFRACTION_USDA-3A1A1A_M/v02",
    250,
)
SOC_IMG = PlanetImage(
    "OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02",
    250,
)
PH_IMG = PlanetImage(
    "OpenLandMap/SOL/SOL_PH-H2O_USDA-4C1A2A_M/v02",
    250,
)
SAND_IMG = PlanetImage(
    "OpenLandMap/SOL/SOL_SAND-WFRACTION_USDA-3A1A1A_M/v02",
    250,
)
SWC_IMG = PlanetImage(
    "OpenLandMap/SOL/SOL_WATERCONTENT-33KPA_USDA-4B1C_M/v01",
    250,
)
