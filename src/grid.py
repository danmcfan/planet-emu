import ee


def create_features_grid(
    min_x: float,
    min_y: float,
    max_x: float,
    max_y: float,
    delta_x: float,
    delta_y: float,
) -> list[ee.Feature]:
    features = []
    id = 0

    x = min_x
    y = min_y

    while x < max_x:
        while y < max_y:
            features.append(
                ee.Feature(
                    ee.Geometry.Rectangle(
                        x,
                        y,
                        x + delta_x,
                        y + delta_y,
                    ),
                    {"id": id},
                ),
            )
            id += 1
            y += delta_y
        x += delta_x
        y = min_y

    return features
