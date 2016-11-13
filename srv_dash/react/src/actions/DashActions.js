import {
    REQUEST_METRICS,
    RECEIVE_METRICS
} from '../constants';

function requestMetrics(app) {
    return {
        type: REQUEST_METRICS,
        app: app
    }
}

function receiveMetris(app, metrics) {
    return {
        type: RECEIVE_METRICS,
        app,
        metrics,
    }
}

export function fetchMetrics(app) {
    return dispatch => {
        dispatch(requestMetrics(app));
        return fetch(`/metrics/${app}`)
            .then(response => response.json())
            .then(json => dispatch(receiveMetris(app, json.metrics)));
    }
}
