import React from 'react';
// Material-ui components
import {RaisedButton, TextField} from 'material-ui';
// React-bootstrap components
import {Col} from 'react-bootstrap/lib/';

const styles = {
	margin: 10
}

class LoginForm extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			email:'',
			password:''
		}
		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleChange(event) {
		if (event.target.name === 'email') 
			this.setState({email: event.target.value, password: this.state.password})
		if (event.target.name === 'password')
			this.setState({	email: this.state.email, password: event.target.value})
	}

	handleSubmit(event) {
		event.preventDefault();
		let emailValue = event.target[0].value.trim();
		let passwordValue = event.target[1].value.trim();
		if (emailValue === '' ){
			alert('email required!');
			return;
		}
		if (passwordValue === '') {
			alert('password required!');
			return;
		}
		if (emailValue === '' || passwordValue === '') {
			alert('Fill the form Asshole!');
			return;
		}
		
		this.props.onLoginSubmit({ email: emailValue, password: passwordValue });
		event.target[0].value = '';
		event.target[1].value = '';
		return;
	}

  render() {
    return (
			<div>
				<h2>Log In</h2>
					<form onSubmit={this.handleSubmit}>
						<Col xs={12} md={4}>
							<TextField
								name="email"
								floatingLabelText="Enter your email"
								onChange={this.handleChange}
								type="email"
								value={this.state.email}
								style={styles}
								/>
						</Col>
						<Col xs={12} md={4}>
							<TextField
								name="password"
								floatingLabelText="Enter your password"
								onChange={this.handleChange}
								type="password"
								value={this.state.comment}
								style={styles}
								/>
						</Col>
						<Col xs={10} xsOffset={1} md={4}>
							<RaisedButton type="submit" label="Submit" primary={true} style={styles} />
						</Col>
					</form>
			</div>
    );
  }

}

export default LoginForm;

LoginForm.propTypes = {
	handleChange: React.PropTypes.func,
	onLoginSubmit: React.PropTypes.func
}