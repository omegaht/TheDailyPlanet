import React, { Component, PropTypes } from 'react';
// Metrial-ui
import { Menu, MainButton, ChildButton } from 'react-mfb';
//Para la conexion con la api
import axios from 'axios';

let effect = 'zoomin',
	pos = 'br',
	method = 'hover';

const MenuLogged = (props) => {
	return (
		<Menu effect={effect} method={method} position={pos}>
			<MainButton iconResting="fa fa-plus" iconActive="fa fa-times" />
				<ChildButton
					icon="fa fa-facebook"
					label="Share on facebook"
					href="https://www.facebook.com/r.php" />
			<ChildButton
				icon="fa fa-twitter"
				label="Share on Twitter"
				href="http://twitter.com/share?text=Amazing MIRA ESTE BETA JORGE!" />
							<ChildButton
				icon="fa fa-user-o"
				label={props.name}
				href="/" />
		</Menu>
	)
}

const MenuNoLogged = () => {
	return (
		<Menu effect={effect} method={method} position={pos}>
			<MainButton iconResting="fa fa-plus" iconActive="fa fa-times" />
			<ChildButton
				icon="fa fa-facebook"
				label="Share on facebook"
				href="https://www.facebook.com/r.php" />

			<ChildButton
				icon="fa fa-twitter"
				label="Share on Twitter"
				href="http://twitter.com/share?text=Amazing MIRA ESTE BETA JORGE!" />
			<ChildButton
				icon="fa fa-user-o"
				label="user"
				href="/" />
		</Menu>
	)
}

export default class RenderMenu extends Component {
	constructor(props) {
		super(props);
		this.state = {
			userName: ''
		}
	}

	componentWillMount(){
		console.log('hola');
		axios.get('/user/info')
		.then(function (response) {
			console.log(response);
			this.setState({userName: response.data.name})
		})
		.catch(function (error) {
			console.log(error);
		});
	}

	render() {
		if (this.state.user == ! null){
			return <MenuLogged name={this.state.userName}/>; 
		}
		return <MenuNoLogged />;
	}
}

MenuLogged.propTypes = {
	name: PropTypes.string,
};