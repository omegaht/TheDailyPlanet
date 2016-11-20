import React from 'react';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

import NavigationBar from './components/NavBar';

var Main = React.createClass({
    render(){
        return (
            <div>
                <MuiThemeProvider>
                    <NavigationBar />
                </MuiThemeProvider>
                <MuiThemeProvider>
                    {this.props.children}
                </MuiThemeProvider>
            </div>
        );
        }
});

export default Main;

Main.propTypes = {
    children: React.PropTypes.element
}
