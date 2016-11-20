import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, hashHistory } from 'react-router';

import Main from './Main';

import injectTapEventPlugin from 'react-tap-event-plugin';

injectTapEventPlugin();

require('./style.css');

ReactDOM.render((
    <Router history={hashHistory}>
        <Route path="/" component={Main}/>
    </Router>
    ), document.getElementById('reactEntry')
);