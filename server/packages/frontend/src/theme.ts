import { purple } from '@material-ui/core/colors';
import { createTheme } from '@material-ui/core/styles';

const muiTheme = createTheme({
  palette: {
    type: 'dark',
    primary: {
      main: '#0052cc',
    },
    secondary: {
      main: '#edf2ff',
    },
    background: {
      default: '#19191c',
    }
  },
});

export default muiTheme;