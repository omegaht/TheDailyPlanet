import React, {Component} from 'react';

import {Menu, MainButton, ChildButton} from 'react-mfb';

let effect = 'zoomin',
    pos = 'br',
method = 'hover';

export default class RenderMenu extends Component {
    render(){
        return(
            <Menu effect={effect} method={method} position={pos}>
                <MainButton iconResting="ion-plus-round" iconActive="ion-close-round" />
                <ChildButton
                    //onClick={function(e){ console.log(e); e.preventDefault(); }}
                    icon="ion-social-github"
                    label="View on Github"
                    href="https://github.com/nobitagit/react-material-floating-button/" />
                <ChildButton
                    icon="ion-social-octocat"
                    label="Follow me on Github"
                    href="https://github.com/nobitagit" />
                <ChildButton
                    icon="ion-social-twitter"
                    label="Share on Twitter"
                    href="http://twitter.com/share?text=Amazing MIRA ESTE BETA JORGE!" />
            </Menu>
        )
    }
}