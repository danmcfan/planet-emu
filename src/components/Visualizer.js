import * as React from 'react';
import Box from '@mui/material/Box';

import MapBox from './MapBox';
import Legend from './Legend';
import LayerSelection from './LayerSelection';
import counties from '../data/counties.geojson';
import summary from '../data/summary.json';

const mainLayerList = [
    { value: "soil", label: "Soil" },
    { value: "weather", label: "Weather" },
    { value: "ndvi", label: "NDVI" },
]

const soilAttributeList = [
    { value: "bulkdens", label: "Bulk Density (10 * kg / m^3)" },
    { value: "clay", label: "Clay Content (%)" },
    { value: "ph", label: "pH Score" },
    { value: "sand", label: "Sand Content (%)" },
    { value: "soc", label: "Soil Organic Carbon (5 * g / kg)" },
    { value: "swc", label: "Soil Water Content (%)" },
]

const weatherAttributeList = [
    { value: "dayl", label: "Day Length (s)" },
    { value: "prcp", label: "Percipitation (mm)" },
    { value: "srad", label: "Solar Radiation (W/m^2)" },
    { value: "swe", label: "Snow Water Equivalent (kg / m^2)" },
    { value: "tmax", label: "Maximum Temperature (C)" },
    { value: "tmin", label: "Minimum Temperature (C)" },
    { value: "vp", label: "Water Vapor Pressure (Pa)" },
]

const ndviAttributeList = [
    { value: "ndvi", label: "True NDVI" },
    { value: "linear_ndvi", label: "Linear Model NDVI" },
    { value: "dnn_ndvi", label: "DNN Model NDVI" },
]

const depthList = [
    { value: "0", label: "0 cm" },
    { value: "10", label: "10 cm" },
    { value: "30", label: "30 cm" },
    { value: "60", label: "60 cm" },
    { value: "100", label: "100 cm" },
    { value: "200", label: "200 cm" },
]

export default function Visualizer() {
    const [layer, setLayer] = React.useState("soil");
    const [attribute, setAttribute] = React.useState("bulkdens");
    const [attributeList, setAttributeList] = React.useState(soilAttributeList);
    const [depth, setDepth] = React.useState("0");
    const [disable, setDisable] = React.useState(false);

    React.useEffect(() => {
        if (layer === "soil") {
            setDisable(false);
            setAttribute("bulkdens");
            setAttributeList(soilAttributeList);
        } else if (layer === "weather") {
            setDisable(true);
            setAttribute("dayl");
            setAttributeList(weatherAttributeList);
        } else if (layer === "ndvi") {
            setDisable(true);
            setAttribute("ndvi");
            setAttributeList(ndviAttributeList);
        }
    }, [layer]);

    return (
        <Box sx={{
            m: 0,
            display: "flex",
            flexDirection: "column",
            justifyContent: "center"
        }}>
            <Box sx={{ m: 0 }}>
                <MapBox layer={layer} attribute={attribute} depth={depth} counties={counties} summary={summary} />
            </Box >
            <Box sx={{ m: 0, display: "flex", flexDirection: "column", justifyContent: "space-around" }}>
                <Legend layer={layer} attribute={attribute} depth={depth} summary={summary} />
                <Box sx={{ mt: 2, display: "flex", flexDirection: "row", justifyContent: "center" }}>
                    <LayerSelection title="Layer" layer={layer} setLayer={setLayer} layerSelectionList={mainLayerList} />
                    <LayerSelection title="Attribute" layer={attribute} setLayer={setAttribute} layerSelectionList={attributeList} />
                    {!disable && <LayerSelection title="Depth" layer={depth} setLayer={setDepth} layerSelectionList={depthList} />}
                </Box>
            </Box>
        </Box >
    );
}