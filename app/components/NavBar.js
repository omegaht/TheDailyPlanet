import React, {Component} from 'react';
import AppBar from 'material-ui/AppBar';
import IconButton from 'material-ui/IconButton';
import IconMenu from 'material-ui/IconMenu';
import MenuItem from 'material-ui/MenuItem';
import SvgIconMenu from 'material-ui/svg-icons/navigation/menu';
import TextField from 'material-ui/TextField';
import SvgIconSearch from 'material-ui/svg-icons/action/search';
// React-router
import {hashHistory} from 'react-router';

const IconMenuController = () => {
    return(
        <IconMenu
            iconButtonElement={<IconButton><SvgIconMenu /></IconButton>}
            targetOrigin={{vertical: 'bottom', horizontal: 'left'}}
            >
            <MenuItem value='1' primaryText='SignIn' onClick={() => {hashHistory.push('/authenticate')}}/>
            <MenuItem value='2' primaryText='LogIn' onClick={() => {hashHistory.push('/authenticate')}} />
        </IconMenu>
    )
}

const IconSearchController = () => { 
    return(
        <div>
            <TextField hintText='Search ...' />
            <IconButton><SvgIconSearch /></IconButton>
        </div>
    )  
}

export default class NavBar extends Component {
    render(){
        return(
             <AppBar
                title='Daily Planet'
                iconElementLeft={<IconMenuController />}
                iconElementRight={<IconSearchController />}
                />  
        )
    }
}