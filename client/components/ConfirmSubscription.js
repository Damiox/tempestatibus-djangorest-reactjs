import React from 'react';
import {Col, Alert} from 'react-bootstrap';

export class ConfirmSubscription extends React.Component {
	constructor(props) {
		super(props);
		this.state = { confirmationSuccess: null };
	}

	componentDidMount() {
		fetch('/api/v1/subscription/' + this.props.match.params.id + '/confirm', {
			method: 'post'
		})
		.then(result => {
			if (result.ok) {
				this.setState({ confirmationSuccess: true });
			} else {
				this.setState({ confirmationSuccess: false });
			}
		});
	}

	render() {
		return (
			<Col smOffset={3} sm={6} mdOffset={4} md={4}>
				{ this.state.confirmationSuccess != null && this.state.confirmationSuccess 
					? <ConfirmSubscriptionSuccess /> : null }
				{ this.state.confirmationSuccess != null && !this.state.confirmationSuccess 
					? <ConfirmSubscriptionError /> : null }
			</Col>
		);
	}
}

class ConfirmSubscriptionSuccess extends React.Component {
	render() {
		return (
			<Alert bsStyle="success">
				<strong>Congratulations!</strong><br />You've been subscribed to this Newsletter.<br />
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
				You may want to try subscribing again <a href="/subscribe-now">now</a>.
			</Alert>
		);
	}
}