import React from 'react';
// React Boostrap components
import {Grid, Row, Col} from 'react-bootstrap/lib';
// Material-ui components
import {List, ListItem} from 'material-ui/List';
import Avatar from 'material-ui/Avatar';

const CommentList = (props) => {
	if(props.data){
		return(
			<Grid>
				<Row>
					<Col xs="{10}">
					<List>
						{
							props.data.map(comment => {
								return(
									<ListItem
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
					</Col>
				</Row>
			</Grid>
			
		); 
	}
	return (<div>"There are no comments to display"</div>);
};

CommentList.propTypes = {
	data: React.PropTypes.array
}

export default CommentList;

							