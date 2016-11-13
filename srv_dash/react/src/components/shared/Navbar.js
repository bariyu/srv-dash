import React from 'react';

import { browserHistory } from 'react-router';

export default class Navbar extends React.Component {
    render() {
        return (
            <nav className="pt-navbar pt-fixed-top pt-dark">
                <div className="pt-navbar-group pt-align-left">
                    <div className="pt-navbar-heading">
                        srv-dash Dashboard
                    </div>
                </div>
                <div className="pt-navbar-group pt-align-right">
                    <button className="pt-button pt-minimal pt-icon-home" onClick={() => browserHistory.push('/')}>
                        Home
                    </button>
                </div>
            </nav>
        )
    }
}
