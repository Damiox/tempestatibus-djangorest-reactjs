import React from 'react';
import {Alert, Col} from 'react-bootstrap';

export class SubscribeReceiptResult extends React.Component {
    constructor(props) {
        super(props);
        this.getResultMessage = this.getResultMessage.bind(this);
    }

    getResultMessage(resultState) {
        switch (resultState) {
            case 'SUCCESS':
                return <SubscribeReceiptSuccess email={ this.props.email } />
            case 'ERROR':
                return <SubscribeReceiptError email={ this.props.email } />
        }
    }

    render() {
        return (
            <div>{ this.getResultMessage(this.props.resultState) }</div>
        );
    }
}

class SubscribeReceiptSuccess extends React.Component {
    render() {
        return (
            <Alert bsStyle="info">
                An e-mail has been sent to <strong>{this.props.email}</strong>. <br />
                Please follow the instructions there to confirm this subscription.<br />
            </Alert>
        );
    }
}

class SubscribeReceiptError extends React.Component {
    render() {
        return (
            <Alert bsStyle="danger">
                Unable to request subscription to <strong>{this.props.email}</strong>. <br />
            </Alert>
        );
    }
}
