import React from 'react';

import {Card, CardHeader, CardTitle, CardMedia, CardText, CardActions} from 'material-ui/Card'
import FlatButton from 'material-ui/FlatButton'

import {Link} from 'react-router'

function Article(props){
	return(
		<Card style={{margin: 20}}>
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
			<CardActions>
				<Link to='/article'><FlatButton label='Ver m&aacute;s' /></Link>
			</CardActions>
		</Card>
	)
}

export default Article;

Article.propTypes = {
	article: React.PropTypes.object,
	src: React.PropTypes.string,
	text: React.PropTypes.string,
	title: React.PropTypes.string,
	category: React.PropTypes.string
}