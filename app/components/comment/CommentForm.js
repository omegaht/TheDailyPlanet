import React, { Component } from 'react';

import {FormControl, FormGroup} from 'react-bootstrap/lib/';
import {Button} from 'react-bootstrap/lib/';
import {Grid, Row, Col} from 'react-bootstrap/lib/';
// export default class CommentForm extends Component{

//     handleSubmit(e){
        
//         e.preventDefault();
        
//         let userValue = e.target[0].value.trim();
//         let textValue = e.target[1].value.trim();

//         if (!textValue || !userValue){
//             return;
//         }

//         this.props.onCommentSubmit({ user: userValue, text: textValue});
//         e.target[0].value = '';
//         e.target[1].value = '';
//         return;
//     }

//     render(){
//         return(
//             <form onSubmit={this.handleSubmit.bind(this)}>
//                  <FormGroup>
//                     <FormControl type="text" placeholder="Name" />
//                     <FormControl type="text" placeholder="comment" />
//                     <Button type="submit"  bsStyle="primary" />
//                 </FormGroup>
//             </form>
//         );
//     }
// }

// CommentForm.propTypes = {
//     onCommentSubmit: React.PropTypes.func
// }



class CommentForm extends Component {
	constructor(props){
			super(props);
			this.handleSubmit = this.handleSubmit.bind(this);
	}
	handleSubmit(event){
		event.preventDefault();
		let nameValue = event.target[0].value.trim();
		let textValue = event.target[1].value.trim();
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
					<Col xs={10}>
						<form onSubmit={this.handleSubmit}>
							<FormGroup>
								<FormControl type="text" placeholder="name" />
								<FormControl type="text" placeholder="comment" />
								<Button type="submit" bsStyle="primary">Submit</Button>
							</FormGroup>
						</form>
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