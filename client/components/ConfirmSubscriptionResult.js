import React from 'react';
import {Alert, Col} from 'react-bootstrap';

export class ConfirmSubscriptionResult extends React.Component {
    constructor(props) {
        super(props);
        this.getResultMessage = this.getResultMessage.bind(this);
    }

    getResultMessage(resultState) {
        switch (resultState) {
            case 'SUCCESS_NEW':
                return <ConfirmSubscriptionSuccessNew />
            case 'SUCCESS_UPDATE':
                return <ConfirmSubscriptionSuccessUpdate />
            case 'ERROR':
                return <ConfirmSubscriptionError />
        }
    }

    render() {
        return (
            <div>{ this.getResultMessage(this.props.resultState) }</div>
        );
    }
}

class ConfirmSubscriptionSuccessNew extends React.Component {
    render() {
        return (
            <Alert bsStyle="success">
                <strong>Congratulations!</strong><br />You've been subscribed to this Newsletter.<br />
                You will be receiving daily emails
            </Alert>
        );
    }
}

class ConfirmSubscriptionSuccessUpdate extends React.Component {
    render() {
        return (
            <Alert bsStyle="success">
                <strong>Done!</strong><br />Your subscription has been updated.<br />
                You will be receiving daily emails
            </Alert>
        );
    }
}

class ConfirmSubscriptionError extends React.Component {
    render() {
        return (
            <Alert bsStyle="danger">
                This confirmation link has expired or it is invalid. <br /> ¯\_(ツ)_/¯ <br />
                You may want to try again <a href="/subscribe-now">now</a>.
            </Alert>
        );
    }
}
