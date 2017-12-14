import React from 'react';
import {getCookie} from '../util';
import {pluck} from 'underscore';
import {Form, FormGroup, FormControl, Col, ControlLabel, Button} from 'react-bootstrap';

export class SubscribeReceiptFormInput extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            locations: [],
            subscriptionEmail: "",
            subscriptionLocation: ""
        };

        this.handleEmailChanged = this.handleEmailChanged.bind(this);
        this.handleLocationChanged = this.handleLocationChanged.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleEmailChanged(event) {
        this.setState({ subscriptionEmail: event.target.value });
    }

    handleLocationChanged(event) {
        this.setState({ subscriptionLocation: event.target.value });
    }

    handleSubmit(event) {
        event.preventDefault();
        this.setState({ subscriptionSuccess: null });

        // Notifying parent about that this form has been successfully completed
        this.props.onFormCompleted(this.state.subscriptionEmail, this.state.subscriptionLocation);
    }

    componentDidMount() {
        fetch('/api/v1/location', {
            method: 'get',
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
        .then(result => result.json())
        .then(locations => this.setState({ locations: pluck(locations, 'city_name') }));
    }

    render() {
        return (
            <Form horizontal onSubmit={this.handleSubmit}>
                <FormGroup>
                    <ControlLabel>Email Address</ControlLabel>
                    <FormControl required type="email" placeholder="Email" onChange={this.handleEmailChanged} />
                </FormGroup>

                <FormGroup>
                    <ControlLabel>Location</ControlLabel>
                    <FormControl required componentClass="select" value={this.state.subscriptionLocation} onChange={this.handleLocationChanged}>
                        <option value="" disabled>Where do you live?</option>
                        {this.state.locations.map(city => <option key={city} value={city}>{city}</option>)}
                    </FormControl>
                </FormGroup>

                <FormGroup>
                    <Col mdOffset={2} md={8}>
                        <Button bsStyle="primary" bsSize="large" type="submit" block>Subscribe</Button>
                    </Col>
                </FormGroup>
            </Form>
        );
    }
}
