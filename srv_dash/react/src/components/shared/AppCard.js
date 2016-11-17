import React from 'react';

import { browserHistory } from 'react-router';

export default class AppCard extends React.Component {
    render() {
        return (
            <div className="pt-card pt-elevation-2 pt-interactive" style={{margin: '10px'}} onClick={() => browserHistory.push(`/dash/${this.props.app}`)}>
                <h5>
                    {this.props.app}
                </h5>
            </div>
        )
    }
}
