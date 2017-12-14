import React from 'react';
import {Alert, Col} from 'react-bootstrap';

export class ConfirmUnsubscriptionResult extends React.Component {
    constructor(props) {
        super(props);
        this.getResultMessage = this.getResultMessage.bind(this);
    }

    getResultMessage(resultState) {
        switch (resultState) {
            case 'SUCCESS':
                return <ConfirmUnsubscriptionSuccess />
            case 'ERROR':
                return <ConfirmUnsubscriptionError />
        }
    }

    render() {
        return (
            <div>{ this.getResultMessage(this.props.resultState) }</div>
        );
    }
}

class ConfirmUnsubscriptionSuccess extends React.Component {
    render() {
        return (
            <Alert bsStyle="success">
                <strong>Done!</strong><br />You've been unsubscribed from this Newsletter.<br />
                Hope to see you back soon :)
            </Alert>
        );
    }
}

class ConfirmUnsubscriptionError extends React.Component {
    render() {
        return (
            <Alert bsStyle="danger">
                This confirmation link has expired or it is invalid. <br /> ¯\_(ツ)_/¯ <br />
            </Alert>
        );
    }
}
