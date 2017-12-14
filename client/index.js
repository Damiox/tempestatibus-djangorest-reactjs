import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Route, Switch, Redirect} from 'react-router-dom';

import {SubscribeReceipt} from './components/SubscribeReceipt';
import {UnsubscribeReceipt} from './components/UnsubscribeReceipt';
import {ConfirmSubscription} from './components/ConfirmSubscription';
import {ConfirmUnsubscription} from './components/ConfirmUnsubscription';


class App extends React.Component {
	render() {
		return (
			<BrowserRouter>
				<div>
					<Switch>
						<Route path='/subscribe-now' component={SubscribeReceipt}></Route>
						<Route path='/unsubscribe/:email' component={UnsubscribeReceipt}></Route>
				        <Route path='/confirm-subscription/:id' component={ConfirmSubscription}></Route>
				        <Route path='/confirm-unsubscription/:id' component={ConfirmUnsubscription}></Route>
						<Redirect from='/' to='/subscribe-now'></Redirect>
					</Switch>
				</div>
			</BrowserRouter>
		)
	}
}


ReactDOM.render(
	<App />,
	document.getElementById('app')
);
