from typing import Any, Optional
from dataclasses import dataclass, field
from matplotlib import pyplot as plt
import geopandas as gpd


@dataclass
class PlanetPlot:
    x: int = 1
    y: int = 1
    title: Optional[str] = None
    figure: Any = field(init=False)
    axis: Any = field(init=False)

    def __post_init__(self):
        self.figure, self.axis = plt.subplots(self.x, self.y)
        if self.title:
            self.figure.suptitle(self.title)

    def add_subplot(
        self,
        gdf: gpd.GeoDataFrame,
        column: str,
        x: int = 0,
        y: int = 0,
        title: Optional[str] = None,
        legend: bool = False,
        cmap: str = "Greens",
        ticks: bool = True,
    ) -> Any:
        if self.x == 1 and self.y == 1:
            ax = self.axis
        else:
            ax = self.axis[x, y]
        gdf.plot(ax=ax, column=column, cmap=cmap, legend=legend)
        if title:
            ax.set_title(title)
        if not ticks:
            ax.set_xticks([])
            ax.set_yticks([])

    def show(self) -> None:
        plt.show()

    def to_png(
        self, basename: str, temp: bool = False, dpi: int = 300
    ) -> None:
        dirname = ".temp" if temp else "data"
        plt.savefig(f"{dirname}/images/{basename}.png", dpi=dpi)
