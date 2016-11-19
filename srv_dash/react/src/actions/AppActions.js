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
        $.ajax({
            url: '/apps',
            type: "GET",
            success: function (data) {
                dispatch(receiveApps(data.apps));
            },
            error: function () {
                alert("failed to get apps");
            }
        });    
    }
}
