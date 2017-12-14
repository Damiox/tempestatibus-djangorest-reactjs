import React from 'react';
import {getCookie} from '../util';
import {Col} from 'react-bootstrap';
import {UnsubscribeReceiptResult} from './UnsubscribeReceiptResult';

export class UnsubscribeReceipt extends React.Component {
    constructor(props) {
        super(props);
        this.state = { email: this.props.match.params.email, resultState: null };
    }

    componentDidMount() {
        fetch('/api/v1/unsubscription', {
            method: 'post',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({ "email": this.state.email })
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
                <UnsubscribeReceiptResult resultState={ this.state.resultState } email={ this.state.email } />
            </Col>
        )
    }
}
