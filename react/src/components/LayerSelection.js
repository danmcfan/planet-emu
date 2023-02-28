import * as React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

export default function LayerSelection(props) {
    const handleChange = (event) => {
        props.setLayer(event.target.value);
    };

    return (
        <Box sx={{ minWidth: 300, mr: 4 }}>
            <FormControl fullWidth>
                <InputLabel id="demo-simple-select-label">{props.title}</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={props.layer}
                    label={props.title}
                    onChange={handleChange}
                >
                    {props.layerSelectionList.map(function (layer) { return <MenuItem value={layer.value}>{layer.label}</MenuItem> })}
                </Select>
            </FormControl>
        </Box>
    );
}