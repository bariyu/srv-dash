import {
    REQUEST_METRICS,
    RECEIVE_METRICS,
    CLEAR_METRICS
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

export function clearMetrics(app) {
    return {
        type: CLEAR_METRICS,
        app
    }
}

export function refreshMetrics(app) {
    return dispatch => {
        dispatch(clearMetrics(app));
        dispatch(fetchMetrics(app));
    }
}

export function fetchMetrics(app) {
    return dispatch => {
        dispatch(requestMetrics(app));
        $.ajax({
            url: `/metrics/${app}`,
            type: "GET",
            success: function (data) {
                dispatch(receiveMetris(app, data.metrics));
            },
            error: function () {
                alert("failed to get metrics");
            }
        });
    }
}
