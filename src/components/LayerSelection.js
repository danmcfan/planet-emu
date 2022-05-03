import * as React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';


const layerSelectionList = [
    { value: "bulkdens", label: "Bulk Density" },
    { value: "clay", label: "Clay Content" },
    { value: "ph", label: "pH Score" },
    { value: "sand", label: "Sand Content" },
    { value: "soc", label: "Soil Organic Carbon" },
    { value: "swc", label: "Soil Water Content" },
]

export default function LayerSelection(props) {
    const handleChange = (event) => {
        props.setLayer(event.target.value);
    };

    return (
        <Box sx={{ minWidth: 240 }}>
            <FormControl fullWidth>
                <InputLabel id="demo-simple-select-label">Soil Layer</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={props.layer}
                    label="Soil Layer"
                    onChange={handleChange}
                >
                    {layerSelectionList.map(function (layer) { return <MenuItem value={layer.value}>{layer.label}</MenuItem> })}
                </Select>
            </FormControl>
        </Box>
    );
}