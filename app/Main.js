import React from 'react';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'

import NavigationBar from './components/NavBar'

var Main = React.createClass({
  render(){
    return (
      <MuiThemeProvider>
        <NavigationBar />
      </MuiThemeProvider>
    );
  }
});

export default Main;

