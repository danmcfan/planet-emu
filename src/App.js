import * as React from 'react';
import Box from '@mui/material/Box';

import ButtonAppBar from './ButtonAppBar';
import LineGraph from './LineGraph';
import Selection from './Selection';
import './App.css';

export default function App() {
  return (
    <div>
      <ButtonAppBar />
      <Box sx={{ m: 5, display: "flex", flexDirection: "row", justifyContent: "center" }}>
        <Box sx={{ m: 10, flexGrow: 2 }}>
          <LineGraph />
        </Box>
        <Box sx={{ m: 5, flexGrow: 2 }}>
          <Selection />
        </Box>
      </Box>
    </div>
  );
}
