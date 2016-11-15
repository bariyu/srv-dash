import React from 'react';

import { connect } from 'react-redux';
import { Spinner } from "@blueprintjs/core";

import { fetchMetrics, clearMetrics } from '../../actions/DashActions';

import renderChart from '../shared/charts/ChartFactory';


class AppDash extends React.Component {
    componentDidMount() {
        const { dash, dispatch, params } = this.props;
        if (!dash[params.app]) {
            dispatch(fetchMetrics(params.app));
        }
    }

    componentDidUpdate() {
        const { dash, dispatch, params } = this.props;
        if (!dash[params.app]) {
            dispatch(fetchMetrics(params.app));
        }
    }

    render() {
        const { dash, params, dispatch } = this.props;
        const appMetrics = dash[params.app];
        const refreshBtnComp = (
            <button type="button" className="pt-button pt-intent-primary" onClick={() => dispatch(clearMetrics(params.app))}>
                Refresh
                <span className="pt-icon-standard pt-icon-refresh pt-align-right"></span>
            </button>
        );
        if (!appMetrics) {
            return (
                <div className="flex-box justify-content-center align-items-center">
                    {refreshBtnComp}
                    <Spinner />
                </div>
            )
        }
        var chartComps = [];
        for (var key in appMetrics) {
            chartComps.push(renderChart(appMetrics[key]));
        }
        return (
            <div>
                <div className="flex-box justify-content-flex-start">
                    {refreshBtnComp}
                </div>
                {chartComps}
            </div>
        )
    }
}

export default connect(
    state => ({dash: state.dash}),
)(AppDash);
