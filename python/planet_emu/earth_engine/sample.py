from copy import deepcopy

import ee
import geopandas as gpd

from planet_emu.earth_engine import image


def sample_regions(
    image_obj: ee.Image, input_gdf: gpd.GeoDataFrame, scale: int
) -> gpd.GeoDataFrame:
    input_gdf = deepcopy(input_gdf)

    i = 0
    final_gdf = None

    while i < len(input_gdf):
        j = i + 5000 if i + 5000 < len(input_gdf) else len(input_gdf)

        print(f"Sampling regions {i} to {j}...")

        batch_gdf = input_gdf.iloc[i:j]
        result_gdf = image.reduce_regions(image_obj, batch_gdf, scale=scale)

        if final_gdf is None:
            final_gdf = result_gdf
        else:
            final_gdf = final_gdf.append(result_gdf, ignore_index=True)

        i = j

    return final_gdf
