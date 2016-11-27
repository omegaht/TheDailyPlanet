import React from 'react';
// Material-ui components
import {RaisedButton, TextField } from 'material-ui';
// React-bootstrap components
import {Col} from 'react-bootstrap/lib';

const styles = {
	margin: 10
}

class SignInForm extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			email:'',
			name: '',
			password:''
		}
		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleChange(event) {
		if (event.target.name === 'email') 
			this.setState({email: event.target.value, password: this.state.password, name: this.state.name})
		if (event.target.name === 'password')
			this.setState({	email: this.state.email, password: event.target.value, name: this.state.name})
		if (event.target.name === 'name')
			this.setState({	email: this.state.email, password: this.state.password, name: event.target.value})
	}

	handleSubmit(event) {
		event.preventDefault();
		let emailValue = event.target[0].value.trim();
		let nameValue = event.target[1].value.trim();
		let passwordValue = event.target[2].value.trim();
		
		if (emailValue === '' ){
			alert('email required!');
			return;
		}
		if (nameValue === '' ){
			alert('name required!');
			return;
		}
		if (passwordValue === '') {
			alert('password required!');
			return;
		}
		if (emailValue === '' || passwordValue === '' || nameValue === '') {
			alert('Fill the form Asshole!');
			return;
		}
		
		this.props.onSignInSubmit({ email: emailValue, password: passwordValue, name: nameValue});
		event.target[0].value = '';
		event.target[1].value = '';
		event.target[2].value = '';
		return;
	}


	render() {
		return (
			<div>
				<h2>Sign In with email</h2>
					<form onSubmit={this.handleSubmit}>
						<Col xs={12} md={12}>
							<TextField
								name="email"
								hintText="Enter your email"
								floatingLabelText="Email"
								onChange={this.handleChange}
								type="text"
								value={this.state.email}
								style={styles}
								/>
						</Col>
						<Col xs={12} md={12}>
							<TextField
								name="name"
								floatingLabelText="Name"
								onChange={this.handleChange}
								type="text"
								value={this.state.comment}
								style={styles}
								/>
						</Col>
						<Col xs={12} md={12}>
							<TextField
								name="password"
								floatingLabelText="Password"
								onChange={this.handleChange}
								type="text"
								value={this.state.comment}
								style={styles}
								/>
						</Col>
						<Col xs={10} xsOffset={1} md={12}>
							<RaisedButton type="submit" label="Submit" primary={true} style={styles} />
						</Col>
					</form>
			</div>
		);
	}

}

export default SignInForm;

SignInForm.propTypes = {
	handleChange: React.PropTypes.func,
	onSignInSubmit: React.PropTypes.func
}
