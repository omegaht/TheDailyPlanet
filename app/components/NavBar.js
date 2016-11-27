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
//Para la conexion con la api
import axios from 'axios';

let doLogOut = (response) => {
    axios.get('/logout')
        .then(function(){
            console.log(response);
            hashHistory.push('/');
        })
        .catch(function (error) {
            // lo mandamos pal carajo si no esta logeado.
            alert('Can\'t close the session');
        });
}

let LogOut = () => {
    //verificar que se encuentre la sesion activa.
    axios.get('/user/info')
        .then(doLogOut)
        .catch(function (error) {
            alert('no active session, can\'t close a closed session imbecil!');
            // lo mandamos pal carajo si no esta logeado.
            hashHistory.push('/');
        });
}

const IconMenuController = () => {
    return(
        <IconMenu
            iconButtonElement={<IconButton><SvgIconMenu /></IconButton>}
            targetOrigin={{vertical: 'bottom', horizontal: 'left'}}
            >
            <MenuItem value='1' primaryText='SignIn/LogIn' onClick={() => {hashHistory.push('/authenticate')}}/>
            <MenuItem value='2' primaryText='LogOut' onClick={LogOut} />
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