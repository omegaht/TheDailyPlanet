import React, { Component } from 'react';
import LoginForm from './LoginForm';
import SignUpForm from './SignUpForm';

import { Tabs, Tab } from 'material-ui/Tabs';
import {Row, Col} from 'react-bootstrap/lib/';

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
        this.handleChange = this.handleChange.bind(this)
    }
 handleChange(value) {
        this.setState({
            value: value,
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
                            <LoginForm/>
                        </div>
                    </Tab>
                    <Tab label="SignIn" value="register">
                        <div>
                            <SignUpForm/>
                        </div>
                    </Tab>
                </Tabs>
            </Col>
        </Row>
        
    );
  }
}

export default Authenticate;