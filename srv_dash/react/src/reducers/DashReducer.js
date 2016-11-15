import {
    RECEIVE_METRICS,
    CLEAR_METRICS
} from '../constants';

export default function dashReducer(state = {}, action) {
    switch (action.type) {
        case RECEIVE_METRICS:
            return Object.assign({}, state, {
                [action.app]: action.metrics
            });
        case CLEAR_METRICS:
            return Object.assign({}, state, {
                [action.app]: null
            });
            return
        default:
            return state;
    }
}
