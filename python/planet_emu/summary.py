from planet_emu import util


def export_summary() -> None:
    counties_gdf = util.from_geojson("counties_full")
    summary_dict = dict()

    df = counties_gdf.drop(
        columns=[
            "fips_code",
            "county_name",
            "county_code",
            "state_name",
            "state_abbv",
            "state_code",
            "geometry",
        ]
    )

    print(df.info())

    for col in df.columns:
        col_dict = dict()
        col_dict["min"] = df[col].min()
        col_dict["max"] = df[col].max()
        summary_dict[col] = col_dict

    util.to_json(summary_dict, "summary")
