import React from 'react';
import ReactDOM from 'react-dom';

import { Router, Route, hashHistory, IndexRoute, browserHistory } from 'react-router';
import RedBox from 'redbox-react';

import DashContainer from './components/fullpage/DashContainer';
import AppsPage from './components/fullpage/AppsPage';

class DashApp extends React.Component {
    render() {
        return (
            <Router history={hashHistory}>
                <Route path="/" component={DashContainer}>
                    <IndexRoute component={AppsPage}/>
                </Route>
            </Router>
        )
    }
}

try {
    ReactDOM.render(<DashApp />, document.getElementById('app'));
} catch(e) {
    console.log(e);
    render(<RedBox error={e} />, document.getElementById('app'));
}
