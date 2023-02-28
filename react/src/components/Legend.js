import * as React from 'react';
import Box from '@mui/material/Box';

import './Legend.css';
import { getColorList } from './util';

export default function Legend(props) {
    let colorList = getColorList(props.layer, props.attribute, props.depth, props.summary);
    let legendItems = [];
    for (let item of colorList) {
        legendItems.push(
            <Box sx={{
                mr: 4,
                display: "flex",
                flexDirection: "row",
                justifyContent: "space-around",
                alignItems: "center",
            }}>
                <Box className="legendBox" sx={{ height: "25px", width: "25px", my: 0, mr: "20px", backgroundColor: item.color }} />
                <p className="legendLabel">{item.value.toFixed(2)}</p>
            </Box>
        );
    }

    return (
        <Box sx={{ m: 0, display: "flex", flexDirection: "row", justifyContent: "center", alignItems: "center" }}>
            {legendItems}
        </Box>
    );
}