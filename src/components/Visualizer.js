import * as React from 'react';
import Box from '@mui/material/Box';

import MapBox from './MapBox';
import LineGraph from './LineGraph';
import LayerSelection from './LayerSelection';
import soilData from '../data/soil_counties.geojson';
import soilSummary from '../data/soil_summary.json';

export default function Visualizer() {
    const [layer, setLayer] = React.useState("bulkdens");
    const [featureProperties, setFeatureProperties] = React.useState(null);

    let featureInfo;
    if (featureProperties) {
        featureInfo = (
            <div>
                <p>{featureProperties.county_name}, {featureProperties.state_abbv}</p>
                <p>{featureProperties.fips_code}</p>
            </div>
        )
    } else {
        featureInfo = (
            <div>
                <p>Select a county to view soil data.</p>
            </div>
        )
    }

    return (
        <Box sx={{
            m: 0,
            display: "flex",
            flexDirection: "column",
            justifyContent: "center"
        }}>
            <Box sx={{ m: 0 }}>
                <MapBox layer={layer} setFeatureProperties={setFeatureProperties} soilData={soilData} soilSummary={soilSummary} />
            </Box >
            <Box sx={{ m: 0, display: "flex", flexDirection: "row", justifyContent: "center" }}>
                <Box sx={{ m: 1 }}>
                    <LineGraph layer={layer} featureProperties={featureProperties} />
                </Box >
                <Box sx={{ m: 2 }}>
                    <LayerSelection layer={layer} setLayer={setLayer} />
                    {featureInfo}
                </Box >
            </Box>
        </Box >
    );
}