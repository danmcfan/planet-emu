import ee
import pandas as pd
import datetime as dt

ee.Initialize()


def get_weather_df(x: float, y: float, year: int) -> pd.DataFrame:
    l8 = ee.ImageCollection("NASA/ORNL/DAYMET_V4")
    point = ee.Geometry.Point([x, y])

    l8_filtered = l8.filterBounds(point).filterDate(
        f"{year}-01-01", f"{year+1}-01-01"
    )
    bands = l8_filtered.toBands()

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
