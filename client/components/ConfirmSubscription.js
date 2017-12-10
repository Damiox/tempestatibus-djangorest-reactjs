import React from 'react';
import {Col, Alert} from 'react-bootstrap';

export class ConfirmSubscription extends React.Component {
	// this.props.match.params.confirmid
	render() {
		return (
                        <Col smOffset={3} sm={6} mdOffset={4} md={4}>
				<Alert bsStyle="success text-center">
					<strong>Congratulations!</strong><br />You've been subscribed to this Newsletter.<br />
					You will be receiving daily emails at 6am
				</Alert>
				<Alert bsStyle="danger text-center">
					This confirmation link has expired or it is invalid. <br /> ¯\_(ツ)_/¯ <br />
					You may want to try subscribing again <a href="/subscribe-now">now</a>.
				</Alert>
			</Col>
		)
	}
}

