import ee

BATCH_SIZE = 5000


def reduce_regions(
    image: ee.Image, input_features: list[ee.Feature], scale: int
) -> list[dict]:
    features = []
    i = 0

    while i < len(input_features):
        j = (
            i + BATCH_SIZE
            if i + BATCH_SIZE < len(input_features)
            else len(input_features)
        )
        output_fc = image.reduceRegions(
            collection=ee.FeatureCollection(input_features[i:j]),
            reducer=ee.Reducer.mean(),
            scale=scale,
            tileScale=1,
            crs="EPSG:4326",
        )
        output_features = output_fc.getInfo()["features"]

        features.extend(output_features)
        i += BATCH_SIZE

    return features
