import React from 'react';
import {pluck} from 'underscore';
import {Alert, Form, FormGroup, FormControl, Col, ControlLabel, Checkbox, Button} from 'react-bootstrap';

export class SubscribeReceipt extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			subscriptionSuccess: null,
			locations: [],
			subscriptionEmail: "",
			subscriptionLocation: ""
		};

		this._handleEmailChanged = this._handleEmailChanged.bind(this);
    	this._handleLocationChanged = this._handleLocationChanged.bind(this);
    	this._handleSubmit = this._handleSubmit.bind(this);
	}

	_handleEmailChanged(event) {
		this.setState({ subscriptionEmail: event.target.value });
	}

	_handleLocationChanged(event) {
		this.setState({ subscriptionLocation: event.target.value });
	}

	_handleSubmit(event) {
		event.preventDefault();

		this.setState({ subscriptionSuccess: null });

		fetch('/api/v1/subscription', {
			method: 'post',
			headers: {'Content-Type':'application/json'},
			body: JSON.stringify({ "email": this.state.subscriptionEmail, "city_name": this.state.subscriptionLocation })
		})
		.then(result => {
			if (result.ok) {
				this.setState({ subscriptionSuccess: true });
			} else {
				this.setState({ subscriptionSuccess: false });
			}
		});
	}

	componentDidMount() {
		fetch('/api/v1/location')
			.then(result => result.json())
			.then(locations => this.setState({ locations: pluck(locations, 'city_name') }));
	}

	render() {
		return (
			<Col smOffset={3} sm={6} mdOffset={4} md={4}>
			  <Form horizontal onSubmit={this._handleSubmit}>
			    <FormGroup>
			      <ControlLabel>Email Address</ControlLabel>
			      <FormControl required type="email" placeholder="Email" onChange={this._handleEmailChanged} />
			    </FormGroup>

			    <FormGroup>
			      <ControlLabel>Location</ControlLabel>
			      <FormControl required componentClass="select" value={this.state.subscriptionLocation} onChange={this._handleLocationChanged}>
			      	<option value="" disabled>Where do you live?</option>
			      	{this.state.locations.map(city => <option key={city} value={city}>{city}</option>)}
			      </FormControl>
			    </FormGroup>

			    <FormGroup>
			      <Col mdOffset={2} md={8}>
			        <Button bsStyle="primary" bsSize="large" type="submit" block>
			          Subscribe
			        </Button>
			      </Col>
			    </FormGroup>
			  </Form>

			  { this.state.subscriptionSuccess != null && this.state.subscriptionSuccess 
			  	? <SubscribeReceiptSuccess email={this.state.subscriptionEmail}/> : null }
			  { this.state.subscriptionSuccess != null && !this.state.subscriptionSuccess 
			  	? <SubscribeReceiptError email={this.state.subscriptionEmail}/> : null }
			</Col>
		)
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
				Unable to subscribe <strong>{this.props.email}</strong>. <br />
			</Alert>
		);
	}
}
