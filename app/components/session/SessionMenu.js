import React, {Component} from 'react';

import {Menu, MainButton, ChildButton} from 'react-mfb';

let effect = 'zoomin',
    pos = 'br',
method = 'hover';

export default class RenderMenu extends Component {
    render(){
        return(
            <Menu effect={effect} method={method} position={pos}>
                <MainButton iconResting="fa fa-plus" iconActive="fa fa-times" />
                <ChildButton
                    //onClick={function(e){ console.log(e); e.preventDefault(); }}
                    icon="fa fa-github-alt"
                    label="View on Github"
                    href="https://github.com/nobitagit/react-material-floating-button/" />
                <ChildButton
                    icon="fa fa-github"
                    label="Follow me on Github"
                    href="https://github.com/nobitagit" />
                <ChildButton
                    icon="fa fa-twitter"
                    label="Share on Twitter"
                    href="http://twitter.com/share?text=Amazing MIRA ESTE BETA JORGE!" />
            </Menu>
        )
    }
}