from planet_emu import predict, util


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
    final_gdf = final_gdf.drop(columns=["geometry"])

    counties_gdf = util.from_geojson("counties")
    counties_gdf = counties_gdf.merge(final_gdf, on="fips_code", how="left")
    counties_gdf = counties_gdf.sort_values("fips_code")

    linear_model = predict.load_model("data/model/linear")
    dnn_model = predict.load_model("data/model/dnn")

    features_df = final_gdf.drop(columns=["fips_code", "ndvi"])
    counties_gdf["linear_ndvi"] = linear_model.predict(features_df).flatten()
    counties_gdf["dnn_ndvi"] = dnn_model.predict(features_df).flatten()

    util.to_csv(final_gdf, "features")
    util.to_csv(counties_gdf, "counties_full")
    util.to_geojson(counties_gdf, "counties_full")
