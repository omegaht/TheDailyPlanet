import React, { Component } from 'react';
// Material-ui components
import {Grid, Row, Col} from 'react-bootstrap/lib/';
import {Card, TextField, RaisedButton} from 'material-ui';

class CommentForm extends Component {
	constructor(props){
			super(props);
			this.state = {
				name: '',
				comment: ''	
			}
			this.handleChange = this.handleChange.bind(this);
			this.handleSubmit = this.handleSubmit.bind(this);
	}
	handleChange(event){
		if (event.target.name === 'name') {
			this.setState(
				{
					name: event.target.value,
					comment: this.state.comment
				}
			)
		}else {
			this.setState(
				{
					name: this.state.name,
					comment: event.target.value
				}
			)
		}
	}
	handleSubmit(event){
		event.preventDefault();
		let nameValue = event.target[0].value.trim();
		let textValue = event.target[1].value.trim();
		if (nameValue === '')
			nameValue = 'Anonymous'

		if (textValue === ''){
				alert('Text is required, no blank comments!');
				return;
		}
		this.props.onCommentSubmit({user: nameValue, text: textValue});
		event.target[0].value = '';
		event.target[1].value = '';
		return; 
	}
	render() {
		return (
			<Grid>
				<Row>
					<Col xs={10} xsOffset={1}>
						<Card	title="Post a Comment">
							<form onSubmit={this.handleSubmit}>
								<TextField
									name="name"
									hintText="Name"
									floatingLabelText="Enter your name"
									onChange={this.handleChange}
									type="text"
									value={this.state.name}
								/><br/>
								<TextField
									name="comment"
									hintText="Comment ..."
									floatingLabelText="Enter your comment"
									onChange={this.handleChange}
									type="text"
									value={this.state.comment}
									fullWidth={true}
								/><br/>
								<RaisedButton type="submit" label="Submit" primary={true} />
							</form>
						</Card>
					</Col>
				</Row>
			</Grid>
		);
	}
}

export default CommentForm;

CommentForm.propTypes = {
    onCommentSubmit: React.PropTypes.func.isRequired,
};