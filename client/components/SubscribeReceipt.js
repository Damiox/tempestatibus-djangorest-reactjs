import React from 'react';
import {getCookie} from '../util';
import {Col} from 'react-bootstrap';
import {SubscribeReceiptFormInput} from './SubscribeReceiptFormInput';
import {SubscribeReceiptResult} from './SubscribeReceiptResult';

export class SubscribeReceipt extends React.Component {
    constructor(props) {
        super(props);
        this.state = { email: null, resultState: null };
        this.onFormCompleted = this.onFormCompleted.bind(this);
    }

    onFormCompleted(subscriptionEmail, subscriptionLocation) {
        this.setState({ email: subscriptionEmail });

        fetch('/api/v1/subscription', {
            method: 'post',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({ "email": subscriptionEmail, "city_name": subscriptionLocation })
        })
        .then(result => {
            if (result.ok) {
                this.setState({ resultState: 'SUCCESS' });
            } else {
                this.setState({ resultState: 'ERROR' });
            }
        });
    }

    render() {
        return (
            <Col smOffset={3} sm={6} mdOffset={4} md={4}>
                <SubscribeReceiptFormInput onFormCompleted={ this.onFormCompleted } />
                <SubscribeReceiptResult resultState={ this.state.resultState } email={ this.state.email } />
            </Col>
        )
    }
}
