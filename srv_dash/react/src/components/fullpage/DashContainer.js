import React from 'react';

export default class DashContainer extends React.Component {
    render() {
        return (
            <div>
                {this.props.children}
            </div>
        )
    }
}
