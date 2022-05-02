import * as React from 'react';
import Box from '@mui/material/Box';

import ButtonAppBar from './ButtonAppBar';
import LineGraph from './LineGraph';
import Selection from './Selection';
import MapBox from './MapBox';
import './App.css';

export default function App() {
  return (
    <div>
      <ButtonAppBar />
      <Box sx={{
        m: 0,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center"
      }}>
        <Box sx={{ m: 2 }}>
          <MapBox />
        </Box >
        <Box sx={{ m: 0, display: "flex", flexDirection: "row", justifyContent: "center" }}>
          <Box sx={{ m: 2 }}>
            <LineGraph />
          </Box >
          <Box sx={{ m: 2 }}>
            <Selection />
          </Box >
        </Box>
      </Box >
    </div >
  );
}
