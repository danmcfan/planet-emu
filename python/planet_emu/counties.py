import warnings

warnings.simplefilter("ignore", FutureWarning)

import geopandas as gpd
import pandas as pd


def clean_counties() -> None:
    counties = gpd.read_file("./data/geojson/raw_counties.geojson")

    counties = counties.drop(
        columns=["countyns", "affgeoid", "lsad", "aland", "awater"]
    ).rename(
        columns={
            "statefp": "state_code",
            "countyfp": "county_code",
            "geoid": "fips_code",
            "name": "county_name",
        }
    )
    counties = counties.loc[
        ~counties.state_code.isin([2, 15, 60, 66, 69, 72, 78])
    ].copy()

    states = pd.read_csv("./data/csv/states.csv", sep=", ", engine="python")

    states = states.rename(
        columns={"stname": "state_name", "st": "state_code", "stusps": "state_abbv"}
    )

    counties = counties.merge(states, on="state_code", how="left")
    counties = counties[
        [
            "fips_code",
            "county_name",
            "county_code",
            "state_name",
            "state_abbv",
            "state_code",
            "geometry",
        ]
    ]

    counties.to_file("./data/geojson/counties.geojson", driver="GeoJSON")
