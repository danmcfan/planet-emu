import { green, blue, red } from '@mui/material/colors';
import { createTheme } from '@mui/material/styles';

// A custom theme for this app
const theme = createTheme({
    palette: {
        primary: {
            main: blue[800],
        },
        secondary: {
            main: green[800],
        },
        error: {
            main: red[800],
        },
    },
});

export default theme;