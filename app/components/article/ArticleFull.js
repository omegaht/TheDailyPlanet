import React, { PropTypes } from 'react';
// Material-ui Componets
import { Card, CardHeader, CardTitle, CardMedia, CardText, CardActions } from 'material-ui/Card';
import IconButton from 'material-ui/IconButton';
import ActionShare from 'material-ui/svg-icons/social/share';
import ActionPrint from 'material-ui/svg-icons/action/print';
import ActionLike from 'material-ui/svg-icons/action/favorite';
import ActionEdit from 'material-ui/svg-icons/content/create';
import Badge from 'material-ui/Badge';
import Avatar from 'material-ui/Avatar';
import List from 'material-ui/List/List';
import ListItem from 'material-ui/List/ListItem';

const styles = {
	wrapper: {
		display: "flex",
		flexWrap: "wrap"
	}
}

const UsersAvatar = ()=> {
	return(
		<List style={styles.wrapper}>
			<ListItem
				disabled={true}
				leftAvatar={<Avatar src="https://s-media-cache-ak0.pinimg.com/originals/49/68/0a/49680a5fd4de1b3bbdf2ca3fe0edf089.jpg" />}
				>
				Author
			</ListItem>
			<ListItem
				disabled={true}
				leftAvatar={<Avatar src="https://s-media-cache-ak0.pinimg.com/originals/49/68/0a/49680a5fd4de1b3bbdf2ca3fe0edf089.jpg" />}
				>
				Editor
			</ListItem>
		</List>	
	);
}

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
				<div dangerouslySetInnerHTML={{ __html: props.article.text }} ></div>
			</CardText>
			<CardActions>
				<IconButton tooltip="share" touch={true} tooltipPosition="top-right">
					<ActionShare />
				</IconButton>
				<IconButton tooltip="print" touch={true} tooltipPosition="top-right">
					<ActionPrint />
				</IconButton>
				<IconButton tooltip="edit" touch={true} tooltipPosition="top-right">
					<ActionEdit />
				</IconButton>
				<Badge
					badgeContent={4}
					primary={true}
					>
					<ActionLike />
				</Badge>
			</CardActions>
			<CardMedia
				children={<UsersAvatar />}
				>
				
			</CardMedia>
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