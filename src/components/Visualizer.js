import * as React from 'react';
import Box from '@mui/material/Box';

import MapBox from './MapBox';
import Legend from './Legend';
import LayerSelection from './LayerSelection';
import soilData from '../data/soil_counties.geojson';
import soilSummary from '../data/soil_summary.json';

export default function Visualizer() {
    const [layer, setLayer] = React.useState("bulkdens");

    return (
        <Box sx={{
            m: 0,
            display: "flex",
            flexDirection: "column",
            justifyContent: "center"
        }}>
            <Box sx={{ m: 0 }}>
                <MapBox layer={layer} soilData={soilData} soilSummary={soilSummary} />
            </Box >
            <Box sx={{ m: 0, display: "flex", flexDirection: "row", justifyContent: "space-around" }}>
                <Box sx={{ mt: 1 }}>
                    <Legend layer={layer} soilSummary={soilSummary} />
                </Box>
                <Box sx={{ my: 2 }}>
                    <LayerSelection layer={layer} setLayer={setLayer} />
                </Box >
            </Box>
        </Box >
    );
}