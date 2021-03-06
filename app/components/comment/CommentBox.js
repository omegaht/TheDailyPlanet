import React, {Component} from 'react';
//Bootstrat-react Components
import { Row, Col } from 'react-bootstrap/lib/';
// Own Components
import CommentForm from './CommentForm';
import CommentList from './CommentList';

class CommentBox extends Component {
	constructor(){
		super();
		this.state = {
			comments: []
		}
		this.handleCommentSubmit = this.handleCommentSubmit.bind(this);
	}
	handleCommentSubmit(comment){
			//asignar key unico para el comentario
			let commentId = getId(this.state);
			//nuevo state , recordar inmutabilidad es la ostia!
			let finalComment = Object.assign({},{id: commentId},comment);
			// nuevo state con el comentario añadido			
			this.setState({
				comments: this.state.comments.concat([finalComment])
			}) 
	}
	componentWillMount(){
		this.setState({
			comments: [
				{ 
					user:"Shawn Spencer", 
					text:"I've heard it both ways",
					id: 0
				},
				{ 
					user:"Burton Guster", 
					text:"You hear about Pluto? That's messed up",
					id: 1
				}
			]
		})
	}

	render() {
		return (
			<Row>
				<Col xs={12}>
					<CommentForm data={this.state.comments} onCommentSubmit={this.handleCommentSubmit} />			
				</Col>
				<Col xs={12}>
					<CommentList data={this.state.comments} />			
				</Col>
			</Row>
		);
	}
}

function getId(state) {
  return state.comments.reduce((maxId, comment) => {
    return Math.max(comment.id, maxId)
  }, -1) + 1
}

export default CommentBox;