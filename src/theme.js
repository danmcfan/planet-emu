import { green, blue, red } from '@mui/material/colors';
import { createTheme } from '@mui/material/styles';

// A custom theme for this app
const theme = createTheme({
    palette: {
        primary: {
            main: green.A700,
        },
        secondary: {
            main: blue.A700,
        },
        error: {
            main: red.A700,
        },
    },
});

export default theme;