import { createStore, applyMiddleware, compose } from 'redux';
import rootReducer from '../reducers';
import createLogger from 'redux-logger';
import thunk from 'redux-thunk';
import DevTools from '../components/DevTools';

const logger = createLogger();

const finalCreateStore = compose(
    // Middleware you want to use in development:
    applyMiddleware(logger, thunk),
    // Required! Enable Redux DevTools with the monitors you chose
    DevTools.instrument()
)(createStore);

export default function configureStore(initialState) {
    const store = finalCreateStore(rootReducer, initialState);
    return store;
}
