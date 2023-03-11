from enum import Enum


class ImageCollectionEnum(str, Enum):
    WEATHER = "weather"
    SPECTRAL = "spectral"

    @property
    def name(self) -> str:
        match self:
            case ImageCollectionEnum.WEATHER:
                return "NASA/ORNL/DAYMET_V4"
            case ImageCollectionEnum.SPECTRAL:
                return "MODIS/061/MOD09GQ"

    @property
    def scale(self) -> int:
        if self == ImageCollectionEnum.WEATHER:
            return 1000

        return 250


class ImageEnum(str, Enum):
    BULK_DENSITY = "bulk_density"
    CLAY = "clay"
    ORGANIC_CARBON = "organic_carbon"
    PH = "ph"
    SAND = "sand"
    WATER_CONTENT = "water_content"

    @property
    def name(self) -> str:
        match self:
            case ImageEnum.BULK_DENSITY:
                return "OpenLandMap/SOL/SOL_BULKDENS-FINEEARTH_USDA-4A1H_M/v02"
            case ImageEnum.CLAY:
                return "OpenLandMap/SOL/SOL_CLAY-WFRACTION_USDA-3A1A1A_M/v02"
            case ImageEnum.ORGANIC_CARBON:
                return "OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02"
            case ImageEnum.PH:
                return "OpenLandMap/SOL/SOL_PH-H2O_USDA-4C1A2A_M/v02"
            case ImageEnum.SAND:
                return "OpenLandMap/SOL/SOL_SAND-WFRACTION_USDA-3A1A1A_M/v02"
            case ImageEnum.WATER_CONTENT:
                return "OpenLandMap/SOL/SOL_WATERCONTENT-33KPA_USDA-4B1C_M/v01"

    @property
    def scale(self) -> int:
        return 250
