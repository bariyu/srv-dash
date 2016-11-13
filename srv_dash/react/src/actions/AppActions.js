import {
    REQUEST_APPS,
    RECEIVE_APPS
} from '../constants';

function requestApps() {
    return {
        type: REQUEST_APPS,
    }
}

function receiveApps(apps) {
    return {
        type: RECEIVE_APPS,
        apps
    }
}

export function fetchApps() {
    return dispatch => {
        dispatch(requestApps());
        return fetch(`/apps`)
            .then(response => response.json())
            .then(json => dispatch(receiveApps(json.apps)));
    }
}
