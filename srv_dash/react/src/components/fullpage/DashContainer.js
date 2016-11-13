import React from 'react';

import Navbar from "../shared/Navbar";

export default class DashContainer extends React.Component {
    render() {
        return (
            <div>
                <Navbar />
                <div className="dash-container">
                    {this.props.children}
                </div>
            </div>
        )
    }
}
