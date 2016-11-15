import React from 'react';

export default class BaseChart extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        const { name, data } = this.props
        return (
            <div>
                <h5>
                    {this.props.app}
                </h5>
            </div>
        )
    }
}
