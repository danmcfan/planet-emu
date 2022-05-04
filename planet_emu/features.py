from planet_emu import util


def export_features() -> None:
    soil_gdf = util.from_geojson("soil_counties").drop(
        columns=["county_name", "county_code", "state_name", "state_abbv", "state_code"]
    )
    weather_gdf = (
        util.from_geojson("weather_2020")
        .loc[
            :,
            [
                "fips_code",
                "dayl",
                "prcp",
                "srad",
                "swe",
                "tmax",
                "tmin",
                "vp",
            ],
        ]
        .copy()
    )
    ndvi_gdf = (
        util.from_geojson("ndvi_2020")
        .loc[:, ["fips_code", "mean"]]
        .rename(columns={"mean": "ndvi"})
    )

    final_gdf = soil_gdf.merge(weather_gdf, on="fips_code", how="left").merge(
        ndvi_gdf, on="fips_code", how="left"
    )
    final_gdf = final_gdf.sort_values("fips_code")

    util.to_csv(final_gdf.drop(columns=["geometry"]), "features")
