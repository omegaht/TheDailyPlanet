import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, hashHistory, IndexRoute } from 'react-router';

import Main from './Main';
import Article from './components/article/Article';
import ArticleList from './components/article/ArticleList';

import injectTapEventPlugin from 'react-tap-event-plugin';

injectTapEventPlugin();

require('./style.css');

ReactDOM.render((
    <Router history={hashHistory}>
        <Route path="/" component={Main}>
            <IndexRoute component={ArticleList} />
            <Route path="/list" component={Article}/>
        </Route>
    </Router>
    ), document.getElementById('reactEntry')
);