import React from 'react';
import {getCookie} from '../util';
import {Col} from 'react-bootstrap';
import {ConfirmSubscriptionResult} from './ConfirmSubscriptionResult';

export class ConfirmSubscription extends React.Component {
    constructor(props) {
        super(props);
        this.state = { confirmationId: this.props.match.params.id, resultState: null };
    }

    componentDidMount() {
        fetch('/api/v1/subscription/' + this.state.confirmationId + '/confirm', {
            method: 'post',
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
        .then(result => {
            if (result.ok) {
                if (result.state == 201) {
                    this.setState({ resultState: 'SUCCESS_NEW' });
                } else {
                    this.setState({ resultState: 'SUCCESS_UPDATE' });
                }
            } else {
                this.setState({ resultState: 'ERROR' });
            }
        });
    }

    render() {
        return (
            <Col smOffset={3} sm={6} mdOffset={4} md={4}>
                <ConfirmSubscriptionResult resultState={ this.state.resultState } />
            </Col>
        );
    }
}
