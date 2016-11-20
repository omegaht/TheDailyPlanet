import React from 'react';
import {Link} from 'react-router';
import {Card, CardTitle, CardText, RaisedButton, TextField} from 'material-ui';

import {Col, Row} from 'react-bootstrap/lib';

class SignUpForm extends React.Component {

  /**
   * Process the form.
   *
   * @param {object} event - the JavaScript event object
   */
  processForm(event) {
    // prevent default action. in this case, action is the form submission event
    event.preventDefault();

    console.log("name:", this.refs.name.getValue());
    console.log("email:", this.refs.email.getValue());
    console.log("password:", this.refs.password.getValue());
  }


  /**
   * Render the component.
   */
  render() {
    return (    
        <Card>
            <Row>
                <Col xs={5} xsOffset={1}>
                    <form action="/" onSubmit={this.processForm.bind(this)}>
                        <h2 className="card-heading">Sign Up</h2>

                        <CardTitle title="Sign Up with Email" />

                        <div className="field-line">
                            <TextField ref="name" floatingLabelText="Name" />
                        </div>

                        <div className="field-line">
                            <TextField ref="email" floatingLabelText="Email" />
                        </div>

                        <div className="field-line">
                            <TextField ref="password" floatingLabelText="Password" type="password" />
                        </div>

                        <div className="button-line">
                            <RaisedButton type="submit" label="Create New Account" primary={true} />
                        </div>
                        <br/>
                    </form>
                </Col>
            </Row>
        </Card>    
    );
  }

}

export default SignUpForm;
