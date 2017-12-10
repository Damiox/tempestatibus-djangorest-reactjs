import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Route} from 'react-router-dom';

import {SubscribeReceipt} from './components/SubscribeReceipt';
import {ConfirmSubscription} from './components/ConfirmSubscription';


class App extends React.Component {
	render() {
		return (
			<BrowserRouter>
				<div>
					<Route exact path='/' component={SubscribeReceipt}></Route>
			                <Route path='/confirm' component={ConfirmSubscription}></Route>
				</div>
			</BrowserRouter>
		)
	}
}


ReactDOM.render(
	<App />,
	document.getElementById('app')
);
