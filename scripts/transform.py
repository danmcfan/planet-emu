import json


def main():
    with open("data/bulkdens.geojson", "r") as f:
        features = json.load(f)["features"]

    for feature in features:
        feature["id"] = int(feature["id"])
        feature["properties"].pop("id")

    with open("data/bulkdens-transform.geojson", "w") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f)


if __name__ == "__main__":
    main()
