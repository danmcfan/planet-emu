import ee


class GridGenerator:
    def __init__(self, scale: int, width: int, height: int):
        self.scale = scale
        self.width = width
        self.height = height

        self.proj = ee.Projection("EPSG:4326").atScale(self.scale).getInfo()

        self.scale_x = self.proj["transform"][0]
        self.scale_y = -self.proj["transform"][4]

        self.crs = self.proj["crs"]

    def create_grids(
        self, xmin: float, ymin: float, xmax: float, ymax: float
    ) -> list[tuple[int, dict]]:
        grids = []
        index = 0
        x = xmin
        y = ymax

        while x < xmax:
            while y > ymin:
                grids.append(
                    (
                        index,
                        {
                            "dimensions": {"width": self.width, "height": self.height},
                            "affineTransform": {
                                "scaleX": self.scale_x,
                                "shearX": 0,
                                "translateX": x,
                                "shearY": 0,
                                "scaleY": self.scale_y,
                                "translateY": y,
                            },
                            "crsCode": self.crs,
                        },
                    )
                )

                y += self.scale_y * self.height
                index += 1

            y = ymax
            x += self.scale_x * self.width

        return grids
