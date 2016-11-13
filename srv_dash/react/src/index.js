import React from 'react';
import ReactDOM from 'react-dom';

import { Provider } from 'react-redux';
import { Router, Route, browserHistory, IndexRoute } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';

import RedBox from 'redbox-react';

import configureStore from './store/index';

const store = configureStore();

const history = syncHistoryWithStore(browserHistory, store);

import DashContainer from './components/fullpage/DashContainer';
import AppsPage from './components/fullpage/AppsPage';
import AppDash from './components/fullpage/AppDash';
import DevTools from './components/DevTools';

class App extends React.Component {
   render() {
       return (
           <Provider store={store}>
               <div>
                   <Router history={history}>
                       <Route path="/" component={DashContainer}>
                           <IndexRoute component={AppsPage}/>
                           <Route path="dash/:app" component={AppDash} />
                       </Route>
                   </Router>
                   <DevTools />
               </div>
           </Provider>
       )
   }
}

try {
    ReactDOM.render(
        <App />,
        document.getElementById('app')
    );
} catch(e) {
    ReactDOM.render(<RedBox error={e} />, document.getElementById('app'));
}
