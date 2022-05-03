from typing import Any
import pickle
import geopandas as gpd


def to_pickle(
    obj: Any,
    basename: str,
    temp: bool = False,
):
    dirname = ".temp" if temp else "data"
    with open(f"{dirname}/pickle/{basename}.pickle", "wb") as f:
        pickle.dump(obj, f)


def from_pickle(
    basename: str,
    temp: bool = False,
) -> Any:
    dirname = ".temp" if temp else "data"
    with open(f"{dirname}/pickle/{basename}.pickle", "rb") as f:
        obj = pickle.load(f)
    return obj


def to_geojson(
    gdf: gpd.GeoDataFrame,
    basename: str,
    temp: bool = False,
) -> None:
    dirname = ".temp" if temp else "data"
    gdf.to_file(f"{dirname}/geojson/{basename}.geojson", driver="GeoJSON")


def from_geojson(
    basename: str,
    temp: bool = False,
) -> gpd.GeoDataFrame:
    dirname = ".temp" if temp else "data"
    return gpd.read_file(f"{dirname}/geojson/{basename}.geojson", driver="GeoJSON")


def to_csv(
    gdf: gpd.GeoDataFrame,
    basename: str,
    temp: bool = False,
) -> None:
    dirname = ".temp" if temp else "data"
    gdf.to_csv(f"{dirname}/csv/{basename}.csv", index=False)
