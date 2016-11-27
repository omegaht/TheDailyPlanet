import React, { Component, PropTypes } from 'react';
// Material-ui Components
import { Grid, Row, Col } from 'react-bootstrap/lib/';
// Own Components
import ArticleFull from './ArticleFull';
import CommentBox from '../comment/CommentBox';

class ArticleBox extends Component {
	constructor() {
		super();
		this.state = {
			article: {}
		}
	}
	componentWillMount() {
		this.setState({
			article:
			{
				src: 'http://www.el-nacional.com/politica/Delcy-Rodriguez-ONU-Foto-Cancilleria_NACIMA20161105_0024_19.jpg',
				title: 'Delcy Rodríguez asegura que la mayoría de los países aplaude logros de Venezuela en DD HH',
				category: 'Politica',
				date: '05/11/2016',
				text: 'La canciller de la República afirmó que en Venezuela nunca han sido violados los derechos de los ciudadanos. Reconoció que el  \'modelo de inclusión está en su punto más bajo\'',
				autorId: 1,
				likes: 6,
				comments: 10,
				id: 1
			}
		})
	}
	render() {
		return (
			<Grid>
				<Row>
					<Col xs={12}>						
						<ArticleFull article={this.state.article} />
					</Col>
					<Col xs={12}>						
						<CommentBox />
					</Col>
				</Row>
			</Grid>
		);
	}
}

ArticleBox.propTypes = {
	article: PropTypes.object,
	src: PropTypes.string,
	title: PropTypes.string,
	category: PropTypes.string,
	date: PropTypes.string,
	text: PropTypes.string,
	autorId: PropTypes.number,
	likes: PropTypes.number,
	comments: PropTypes.number,
	id: PropTypes.number
};

export default ArticleBox;