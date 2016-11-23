import React from 'react';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

import NavigationBar from './components/NavBar';
import DailyLogo from './components/logo/DailyLogo';

import RenderMenu from './components/session/SessionMenu';

var Main = React.createClass({
    render(){
        return (
            <div>
                <MuiThemeProvider>
                    <NavigationBar />
                </MuiThemeProvider>
                <DailyLogo />
                <MuiThemeProvider>
                    {this.props.children}
                </MuiThemeProvider>
                <RenderMenu />

            </div>
        );
        }
});

export default Main;

Main.propTypes = {
    children: React.PropTypes.element
}
