import React from 'react';
import {Alert, Form, FormGroup, FormControl, Col, ControlLabel, Checkbox, Button} from 'react-bootstrap';

export class SubscribeReceipt extends React.Component {
	render() {
		return (
			<Col smOffset={3} sm={6} mdOffset={4} md={4}>
			  <Form horizontal>
			    <FormGroup>
			      <ControlLabel>Email Address</ControlLabel>
			      <FormControl type="email" placeholder="Email" />
			    </FormGroup>

			    <FormGroup>
			      <ControlLabel>Location</ControlLabel>
			      <FormControl componentClass="select">
				<option value="" selected disabled>Where do you live?</option>
				<option value="tz1">America/NYC</option>
				<option value="tz2">America/Seattle</option>
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

			  <Alert bsStyle="info text-center">
			    An e-mail has been sent to <strong>email@email.com</strong>. Please follow the instructions there to confirm this subscription.<br />
			    You want to subscribe another email? Click <a href="/subscribe-now">Here</a>.
			  </Alert>
			</Col>
		)
	}
}

