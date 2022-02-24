import React, { useContext, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { BrowserRouter, Redirect, Route, Switch } from 'react-router-dom';
import { GlobalStyle } from './components/GlobalStyle';
import { Layout } from './components/Layout';
import './css/App.css';
import { DashboardPage } from './pages/Dashboard/DashboardPage2';
import muiTheme from './theme';
import background from './assets/background2.png';
import { createTheme, ThemeProvider } from '@material-ui/core';
import { roomContext, RoomProvider } from './contexts/RoomContext';

export const BasePage = () => {
  return <Redirect to='/dashboard' />;
};

//<div style={{ backgroundImage: `url(${background})` }}>
export const App = () => {  
  return (
    <div>
      <ThemeProvider theme={muiTheme}>
        <RoomProvider>
          <BrowserRouter>
            <Layout>
              <Switch>
                <Route exact path='/Dashboard' component={DashboardPage} />
                <Route path='/' component={BasePage} />
              </Switch>
            </Layout>
          </BrowserRouter>
        </RoomProvider>
      </ThemeProvider>
    </div>
  );
};

export default App;
