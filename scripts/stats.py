import json
from collections import defaultdict


def main():
    values = defaultdict(list)

    with open("data/final/grid.geojson", "r") as f:
        features = json.load(f)["features"]

    for feature in features:
        properties = feature["properties"]
        for property, value in properties.items():
            if value is not None:
                values[property].append(value)

    for property, value_list in values.items():
        print(property.upper())
        print("Minimum:", min(value_list))
        print("Average:", sum(value_list) / len(value_list))
        print("Maximum:", max(value_list))
        print()


if __name__ == "__main__":
    main()
