import React from 'react';

import { connect } from 'react-redux';

import { fetchMetrics } from '../../actions/DashActions';


class AppDash extends React.Component {
    componentDidMount() {
        const { dash, dispatch, params } = this.props;
        if (!dash[params.app]) {
            dispatch(fetchMetrics(params.app));
        }
    }

    render() {
        const { dash, params } = this.props;
        return (
            <div className="flex-box justify-content-space-between">
                {params.app}
            </div>
        )
    }
}

export default connect(
    state => ({dash: state.dash}),
)(AppDash);
