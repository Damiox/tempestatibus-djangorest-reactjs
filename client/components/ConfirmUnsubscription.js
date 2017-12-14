import React from 'react';
import {getCookie} from '../util';
import {Col} from 'react-bootstrap';
import {ConfirmUnsubscriptionResult} from './ConfirmUnsubscriptionResult';

export class ConfirmUnsubscription extends React.Component {
    constructor(props) {
        super(props);
        this.state = { confirmationId: this.props.match.params.id, resultState: null };
    }

    componentDidMount() {
        fetch('/api/v1/unsubscription/' + this.state.confirmationId + '/confirm', {
            method: 'post',
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
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
                <ConfirmUnsubscriptionResult resultState={ this.state.resultState } />
            </Col>
        );
    }
}
