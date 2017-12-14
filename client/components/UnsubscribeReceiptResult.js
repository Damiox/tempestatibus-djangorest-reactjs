import React from 'react';
import {Alert, Col} from 'react-bootstrap';

export class UnsubscribeReceiptResult extends React.Component {
    constructor(props) {
        super(props);
        this.getResultMessage = this.getResultMessage.bind(this);
    }

    getResultMessage(resultState) {
        switch (resultState) {
            case 'SUCCESS':
                return <UnsubscribeReceiptSuccess email={ this.props.email } />
            case 'ERROR':
                return <UnsubscribeReceiptError email={ this.props.email } />
        }
    }

    render() {
        return (
            <div>{ this.getResultMessage(this.props.resultState) }</div>
        );
    }
}

class UnsubscribeReceiptSuccess extends React.Component {
    render() {
        return (
            <Alert bsStyle="info">
                An e-mail has been sent to <strong>{this.props.email}</strong>. <br />
                Please follow the instructions there to confirm this unsubscription.<br />
            </Alert>
        );
    }
}

class UnsubscribeReceiptError extends React.Component {
    render() {
        return (
            <Alert bsStyle="danger">
                Unable to request unsubscription to <strong>{this.props.email}</strong>. <br />
            </Alert>
        );
    }
}
