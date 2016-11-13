import { combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux'
import appReducer from './AppReducer';
import dashReducer from './dashReducer';


const rootReducer = combineReducers({
    routing: routerReducer,
    apps: appReducer,
    dash: dashReducer
});

export default rootReducer;
