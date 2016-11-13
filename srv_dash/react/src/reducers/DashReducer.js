import {
    RECEIVE_METRICS
} from '../constants';

export default function dashReducer(state = {}, action) {
    switch (action.type) {
        case RECEIVE_METRICS:
            return Object.assign({}, state, {
                [action.app]: action.metrics
            });
        default:
            return state;
    }
}
