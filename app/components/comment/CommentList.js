import React from 'react';
// Material-ui components
import {List, ListItem} from 'material-ui/List';
import Avatar from 'material-ui/Avatar';

const CommentList = (props) => {
	if(props.data){
		return(
			<List>
				{
					props.data.map(comment => {
						return(
							<ListItem
								key={comment.id}
								leftAvatar={<Avatar src="http://static.zerochan.net/Himura.Kenshin.full.551192.jpg" />}
								primaryText={comment.user}
								secondaryText={
									<p>{comment.text}</p>
								}
							/>
							);
					})
				}
			</List>
		); 
	}
	return (<div>"There are no comments to display"</div>);
};

CommentList.propTypes = {
	data: React.PropTypes.array
}

export default CommentList;

							