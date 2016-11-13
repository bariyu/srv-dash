import React from 'react';

import { connect } from 'react-redux'
import { Spinner } from "@blueprintjs/core";

import { fetchApps } from '../../actions/AppActions';
import AppCard from '../shared/AppCard';


class AppsPage extends React.Component {
    componentDidMount() {
        const { apps, dispatch } = this.props;
        if (!apps) {
            dispatch(fetchApps());
        }
    }

    render() {
        const { apps } = this.props;
        if (!apps) {
            return (
                <div className="flex-box justify-content-center align-items-center">
                    <Spinner />
                </div>
            )
        }
        var appCards = apps.map(function(app, idx) {
            return <AppCard app={app} key={idx} />
        })
        return (
            <div>
                <h4>
                    Select an application below to see its dashboard.
                </h4>
                <div className="flex-box justify-content-space-between">
                    {appCards}
                </div>
            </div>
        )
    }
}

export default connect(
    state => ({apps: state.apps}),
)(AppsPage);
