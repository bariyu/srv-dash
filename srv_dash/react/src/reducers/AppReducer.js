import {
    RECEIVE_APPS
} from '../constants';

export default function appReducer(state = null, action) {
    switch (action.type) {
        case RECEIVE_APPS:
            return action.apps;
        default:
            return state;
    }
}
