import * as React from 'react';
import Box from '@mui/material/Box';

import ButtonAppBar from './ButtonAppBar';
import LineGraph from './LineGraph';
import Selection from './Selection';
import Example from './Example';
import './App.css';

export default function App() {
  return (
    <div>
      <ButtonAppBar />
      <Box sx={{ m: 4, display: "flex", flexDirection: "row", justifyContent: "center" }}>
        <Box sx={{ m: 2, flexGrow: 1 }}>
          <Example />
        </Box>
        <Box sx={{ m: 2, flexGrow: 1 }}>
          <LineGraph />
        </Box>
        <Box sx={{ m: 2, flexGrow: 1 }}>
          <Selection />
        </Box>
      </Box>
    </div>
  );
}
