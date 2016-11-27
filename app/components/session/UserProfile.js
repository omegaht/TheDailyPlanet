import React, { Component, PropTypes } from 'react';
import { hashHistory } from 'react-router';
import { RaisedButton, TextField } from 'material-ui';
import Avatar from 'material-ui/Avatar';
import Paper from 'material-ui/Paper';
// React-bootstrap components
import { Grid, Row, Col } from 'react-bootstrap/lib';
//Para la conexion con la api
import axios from 'axios';

const styles = {
  height: 100,
  width: 100,
  margin: 20,
  textAlign: 'center',
  display: 'inline-block'
};
const stylesTextField = {
  margin: 10
}

const ProfilePicture = () => {
  return (
    <Avatar src="http://static.zerochan.net/Himura.Kenshin.full.551192.jpg" size={100} />
  );
}

class UserProfile extends Component {
  constructor() {
    super();
    this.state = {
      proceed: false,
      email: 'Jhon@gmail.com',
      name: 'Jhon Doe',
      type: 'admin',
      password: 123,
      oldEmail: ''
    }

    this.handleChange = this.handleChange.bind(this);
    this.enterUser = this.enterUser.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  enterUser(response){
    this.setState({ proceed: true, email: response.data.email, name: response.data.name, type: response.data.type , oldEmail: response.data.email});
  }

  componentWillMount() {
    //verificar que se encuentre la sesion activa.
    axios.get('/user/info')
      .then(this.enterUser)
      .catch(function (error) {
        alert('no active session, can\'t acces profile page');
        // lo mandamos pal carajo si no esta logeado. (al main) quiero entrenar coño!
        hashHistory.push('/');
      });
  }

  handleChange(event) {
    if (this.state.proceed === true) {
      if (event.target.name === 'email')
        this.setState({ email: event.target.value, type: this.state.type, name: this.state.name, password: this.state.password })
      if (event.target.name === 'type')
        this.setState({ email: this.state.email, type: event.target.value, name: this.state.name, password: this.state.password })
      if (event.target.name === 'name')
        this.setState({ email: this.state.email, type: this.state.type, name: event.target.value, password: this.state.password })
      if (event.target.name === 'name')
        this.setState({ email: this.state.email, type: this.state.type, name: event.target.value, password: event.target.value })
    } else {
      alert('no active session bitch!');
      return;
    }
  }

  handleSubmit(event) {
    event.preventDefault();
    if (this.state.proceed === true) {
      let emailValue = event.target[0].value.trim();
      let nameValue = event.target[1].value.trim();
      let typeValue = event.target[2].value.trim();
      let passwordValue = event.target[3].value.trim();

      if (emailValue === '') {
        alert('email required!');
        return;
      }
      if (nameValue === '') {
        alert('name required!');
        return;
      }
      if (typeValue === '') {
        alert('password required!');
        return;
      }
      if (passwordValue === '') {
        alert('password required!');
        return;
      }
      if (emailValue === '' || typeValue === '' || nameValue === '' || passwordValue === '') {
        alert('Fill the form Asshole!');
        return;
      }
      // envio la data con el api
      axios.post('/user/edit', {
        email: this.state.oldEmail,
        newEmail: this.state.email,
        newName: this.state.name,
        newPassword: this.state.password,
        newType: this.state.type
      })
        .then(function (response) {
          alert('Information updated');
          hashHistory.push('/');
        })
        .catch(function (error) {
        });
      event.target[0].value = '';
      event.target[1].value = '';
      event.target[2].value = '';
      event.target[3].value = '';
      return;

    } else {
      alert('no active session bitch!');
      return;
    }
  }

  render() {
    return (
      <Grid className="UserProfile">
        <Row>
          <h2>Welcome {this.state.name}!</h2>
          <form onSubmit={this.handleSubmit}>
            <Col xs={12} md={5} mdOffset={4}>
              <Paper style={styles} zDepth={4} circle={true} children={<ProfilePicture />} />
            </Col>
            <Col xs={12} md={5} mdOffset={4}>
              <TextField
                name="email"
                hintText="Enter your email"
                floatingLabelText="Email"
                onChange={this.handleChange}
                type="text"
                value={this.state.email}
                style={stylesTextField}
                />
            </Col>
            <Col xs={12} md={5} mdOffset={4}>
              <TextField
                name="name"
                floatingLabelText="Name"
                onChange={this.handleChange}
                type="text"
                value={this.state.name}
                style={stylesTextField}
                />
            </Col>
            <Col xs={12} md={5} mdOffset={4}>
              <TextField
                name="type"
                floatingLabelText="Type"
                onChange={this.handleChange}
                type="text"
                value={this.state.type}
                style={stylesTextField}
                />
            </Col>
            <Col xs={12} md={5} mdOffset={4}>
              <TextField
                name="password"
                floatingLabelText="Password"
                onChange={this.handleChange}
                type="text"
                value={this.state.password}
                style={stylesTextField}
                />
            </Col>
            <Col xs={10} xsOffset={1} md={5} mdOffset={4}>
              <RaisedButton type="submit" label="Edit" primary={true} />
            </Col>
          </form>
        </Row>
      </Grid>
    );
  }
}

UserProfile.propTypes = {
  handleChange: PropTypes.func,
  styles: PropTypes.object,

};

export default UserProfile;