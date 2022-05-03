import * as React from 'react';
import Box from '@mui/material/Box';

import './Legend.css';
import { getColorList } from './util';

export default function Legend(props) {
    let colorList = getColorList(props.layer, props.soilSummary);
    let legendItems = [];
    for (let item of colorList) {
        legendItems.push(
            <Box sx={{
                m: 0,
                display: "flex",
                flexDirection: "row",
                justifyContent: "space-between",
                alignItems: "center",
            }}>
                <Box className="legendBox" sx={{ my: 0, mx: 2, backgroundColor: item.color }} />
                <p>{item.value.toFixed(2)}</p>
            </Box>
        );
    }

    return (
        <div>
            {legendItems}
        </div>
    );
}