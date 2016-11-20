import React from 'react';
import {Link} from 'react-router';
import {Card, CardTitle, CardText, RaisedButton, TextField} from 'material-ui';


import {Col, Row} from 'react-bootstrap/lib/';


class LoginForm extends React.Component {

  /**
   * Process the form.
   *
   * @param {object} event - the JavaScript event object
   */
  processForm(event) {
    // prevent default action. in this case, action is the form submission event
    event.preventDefault();

    // console.log("email:", this.refs.email.getValue());
    // console.log("password:", this.refs.password.getValue());
  }


  /**
   * Process the form.
   *
   * @param {object} event - the JavaScript event object
   */
  render() {
    return (
        <Card >
            <Row>
                <Col xs={6} xsOffset={1}>
                    {/*<form action="/" onSubmit={this.processForm.bind(this)}>*/}
                    <form>
                        <h2 className="card-heading">Log In</h2>

                        <CardTitle title="Login with Email" />

                        <div className="field-line">
                            <TextField ref="email" floatingLabelText="Email" />
                        </div>

                        <div className="field-line">
                            <TextField ref="password" floatingLabelText="Password" type="password" />
                        </div>

                        <div className="button-line">
                            <RaisedButton type="submit" label="Login" primary={true} />
                        </div>
                                                    <br/>
                    </form>
                </Col>
            </Row>
        </Card>
    );
  }

}

export default LoginForm;

LoginForm.propTypes = {
   handleChange: React.PropTypes.func
}