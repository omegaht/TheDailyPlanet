import React from 'react';
// Metrial-ui
import { Menu, MainButton, ChildButton } from 'react-mfb';

let effect = 'zoomin', pos = 'br', method = 'hover';

const RenderMenu = () => {
	return (
		<Menu effect={effect} method={method} position={pos}>
			<MainButton iconResting="fa fa-plus" iconActive="fa fa-times" />
			<ChildButton
				icon="fa fa-facebook"
				label="Share on facebook"
				href="https://www.facebook.com/r.php" />
			<ChildButton
				icon="fa fa-twitter"
				label="Share on Twitter"
				href="http://twitter.com/share?text=Amazing MIRA ESTE BETA JORGE!" />
			<ChildButton
				icon="fa fa-user-o"
				label="user"
				href="/#/profile" />
		</Menu>
	)
};

export default RenderMenu;