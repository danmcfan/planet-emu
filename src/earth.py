import ee
import pandas as pd
import datetime as dt

ee.Initialize()


def get_weather_df(x: float, y: float, year: int) -> pd.DataFrame:
    img = ee.ImageCollection("NASA/ORNL/DAYMET_V4")
    point = ee.Geometry.Point([x, y])

    img_filtered = img.filterBounds(point).filterDate(
        f"{year}-01-01", f"{year+1}-01-01"
    )
    bands = img_filtered.toBands()

    features = bands.sample(
        region=point, geometries=True, scale=1000
    ).getInfo()["features"]

    if len(features) != 1:
        raise ValueError(
            f"Number of features is greater than one: {len(features)}"
        )

    feature = features[0]

    rows = list()

    for k, v in feature["properties"].items():
        date, band = k.split("_")
        date = dt.datetime.strptime(date, "%Y%m%d")
        rows.append(dict(date=date, band=band, value=v))

    df = pd.DataFrame(rows)

    df = df.pivot(index="date", columns="band", values="value").reset_index()

    return df


def get_crop_df(x: float, y: float) -> pd.DataFrame:
    img = ee.ImageCollection("USDA/NASS/CDL")
    point = ee.Geometry.Point([x, y])

    img_filtered = img.filterBounds(point)
    bands = img_filtered.toBands()

    features = bands.sample(region=point, geometries=True, scale=30).getInfo()[
        "features"
    ]

    if len(features) != 1:
        raise ValueError(
            f"Number of features is greater than one: {len(features)}"
        )

    feature = features[0]

    rows = list()

    for k, v in feature["properties"].items():
        year, band = k.split("_")
        year = int(year.replace("a", ""))
        rows.append(dict(year=year, band=band, value=v))

    df = pd.DataFrame(rows)

    df = df.pivot(index="year", columns="band", values="value").reset_index()

    return df


def get_sentinel_df(x: float, y: float) -> pd.DataFrame:
    img = ee.ImageCollection("COPERNICUS/S2")
    point = ee.Geometry.Point([x, y])

    img_filtered = img.filterBounds(point).filterDate(
        "2021-01-01", "2022-01-01"
    )
    bands = img_filtered.toBands()

    features = bands.sample(region=point, geometries=True, scale=60).getInfo()[
        "features"
    ]

    if len(features) != 1:
        raise ValueError(f"Number of features is not 1: {len(features)}")

    feature = features[0]

    rows = list()

    for k, v in feature["properties"].items():
        start, stop, code, band = k.split("_")
        start = dt.datetime.strptime(start, "%Y%m%dT%H%M%S")
        stop = dt.datetime.strptime(stop, "%Y%m%dT%H%M%S")
        rows.append(
            dict(start=start, stop=stop, code=code, band=band, value=v)
        )

    print(feature["geometry"]["coordinates"])

    df = pd.DataFrame(rows)

    df = df.pivot(
        index=["start", "stop", "code"], columns="band", values="value"
    ).reset_index()

    return df
