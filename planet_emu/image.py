from typing import Optional, List, Dict
from dataclasses import dataclass, field
import ee
import eeconvert
import geopandas as gpd
from dotenv import load_dotenv
import os

from planet_emu import gee

load_dotenv()

NAME = os.getenv("GCP_SERVICE_NAME")
PROJECT = os.getenv("GCP_PROJECT")

gee.init(NAME, PROJECT)


@dataclass
class PlanetImageCollection:
    name: str
    scale: int

    def __post_init__(self):
        self.image_collection = ee.ImageCollection(self.name)

    def list_images_info(self) -> List[Dict]:
        return self.image_collection.toList(
            self.image_collection.size()
        ).getInfo()

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

    def get_image_info(self) -> Dict:
        return self.image.getInfo()

    def reduce_regions(
        self,
        in_gdf: gpd.GeoDataFrame,
        mode: bool = False,
    ) -> gpd.GeoDataFrame:
        in_fc = eeconvert.gdfToFc(in_gdf)

        if mode:
            reducer = ee.Reducer.mode()
        else:
            reducer = (
                ee.Reducer.mean()
                .combine(ee.Reducer.stdDev(), sharedInputs=True)
                .combine(ee.Reducer.min(), sharedInputs=True)
                .combine(ee.Reducer.median(), sharedInputs=True)
                .combine(ee.Reducer.max(), sharedInputs=True)
            )

        out_fc = self.image.reduceRegions(
            in_fc,
            reducer=reducer,
            scale=self.scale,
            crs="EPSG:4326",
        )
        return eeconvert.fcToGdf(out_fc)


WEATHER_IC = PlanetImageCollection(
    "NASA/ORNL/DAYMET_V4",
    1000,
)
SENTINEL_IC = PlanetImageCollection(
    "COPERNICUS/S2_SR_HARMONIZED",
    10,
)
CROP_IC = PlanetImageCollection(
    "USDA/NASS/CDL",
    30,
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
