import React, {PropTypes} from 'react';
// Material-ui Componets
import {Card, CardHeader, CardTitle, CardMedia, CardText} from 'material-ui/Card';

const ArticleFull = props => {
	return (
		<Card>
			<CardHeader
				title={'Test'}
				subtitle='Subtitle'
				avatar='https://s-media-cache-ak0.pinimg.com/originals/49/68/0a/49680a5fd4de1b3bbdf2ca3fe0edf089.jpg'
				/>
			<CardTitle
				title={props.article.title}
				subtitle={props.article.category}
				/>
			<CardMedia>
				<img src={props.article.src} />
			</CardMedia>
			<CardText>
				<div dangerouslySetInnerHTML={{__html: props.article.text}} ></div>
			</CardText>
		</Card>
	);
};

ArticleFull.propTypes = {
	article: PropTypes.object,
	title: PropTypes.string,
	category: PropTypes.string,
	src: PropTypes.string,
};

export default ArticleFull;