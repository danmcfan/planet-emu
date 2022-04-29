import * as React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';


const attributeSelection = [
    { value: "bulkdens", label: "Bulk Density" },
    { value: "clay", label: "Clay Content" },
    { value: "ph", label: "pH Score" },
    { value: "sand", label: "Sand Content" },
    { value: "soc", label: "Soil Organic Carbon" },
    { value: "swc", label: "Soil Water Content" },
]

export default function Selection() {
    const [attribute, setAttribute] = React.useState("bulkdens");

    const handleChange = (event) => {
        setAttribute(event.target.value);
    };

    return (
        <Box sx={{ minWidth: 240 }}>
            <FormControl fullWidth>
                <InputLabel id="demo-simple-select-label">Attribute</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={attribute}
                    label="Attribute"
                    onChange={handleChange}
                >
                    {attributeSelection.map(function (attribute) { return <MenuItem value={attribute.value}>{attribute.label}</MenuItem> })}
                </Select>
            </FormControl>
        </Box>
    );
}