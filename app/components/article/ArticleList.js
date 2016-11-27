import React, { Component } from 'react';
import Article from './Article';

import { Row, Col } from 'react-bootstrap/lib/';

import axios from 'axios';

const articleComponent = article => (
	<Col xs={3} key={article.id}>
		<Article article={article} />
	</Col>
)


export default class ArticleList extends Component {
	constructor(props) {
		super(props);

		this.state = {
			articles: [{
				src: 'http://as01.epimg.net/futbol/imagenes/2016/11/24/primera/1480006940_689084_1480007611_noticia_normal.jpg',
				title: 'Loading...',
				category: 'Loading..',
				date: 'Loading..',
				text: '...',
				autorId: 0,
				likes: 0,
				comments: 0,
				id: 1
			}]
		};

		this.setValueOnResponse = this.setValueOnResponse.bind(this)
	}

	setValueOnResponse(response) {
		var articles = response.data.articles;

		this.setState({ articles });

	}

	componentDidMount() {
		axios.get('/article/feed')
			.then(this.setValueOnResponse)
			.catch(function (error) {

			});
	}

	render() {
		return (
			<Row>
				{this.state.articles.map(article => articleComponent(article))}
			</Row>
		)
	}
}

ArticleList.propTypes = {
	articles: React.PropTypes.array,
	children: React.PropTypes.any
}