import React, { Component } from 'react';
// Own Components
import LoginForm from './LoginForm';
import SignInForm from './SignInForm';
// Material-ui
import { Tabs, Tab } from 'material-ui/Tabs';
// React-Boostrap
import { Row, Col } from 'react-bootstrap/lib/';
// React-router
import {hashHistory} from 'react-router';
//Para la conexion con la api
import axios from 'axios';

const styles = {
	headline: {
		fontSize: 24,
		paddingTop: 16,
		marginBottom: 12,
		fontWeight: 400,
	},
	tabs: {
		paddingTop: 50
	}
};

class Authenticate extends Component {
	constructor(props) {
		super(props);
		this.state = {
			value: 'login',
		};
		this.handleChange = this.handleChange.bind(this);
		this.handleLogInSubmit = this.handleLogInSubmit.bind(this);
		this.handleSignInSubmit = this.handleSignInSubmit.bind(this);
	}
	// Manejo de tabs.
	handleChange(value) {
		this.setState({
			value: value,
		});
	}
	handleLogInSubmit(user) {
		// me conecto con la api para hacer la peticion enviando el user.email user.password .
		axios.post('/login', {
			email: user.email,
			password: user.password
		})
		.then(function (response) {
			hashHistory.push('/');
		})
		.catch(function (error) {
		});
	}

	handleSignInSubmit(user) {
		// me conecto con la api para hacer la peticion enviando el user.name user.email user.password2.
		axios.post('/sigin', {
			name: user.name,
			email: user.email,
			password: user.password
		})
		.then(function (response) {
			alert('sucessfull, you are now registerd!');
		})
		.catch(function (error) {

		});
	}

	render() {
		return (
			<Row>
				<Col xs={6} xsOffset={3}>
					<Tabs
						value={this.state.value}
						onChange={this.handleChange}
						style={styles.tabs}
						>
						<Tab label="Login" value="login" >
							<div>
								<LoginForm  onLoginSubmit={this.handleLogInSubmit} />
							</div>
						</Tab>
						<Tab label="SignIn" value="register">
							<div>
								<SignInForm onSignInSubmit={this.handleSignInSubmit}/>
							</div>
						</Tab>
					</Tabs>
				</Col>
			</Row>

		);
	}
}

export default Authenticate;