import React from 'react';
import ReactDOM from 'react-dom';

class App extends React.Component {
	render() {
		return <div>Hi, It's App with Dev SERVER '{ this.props.name + this.props.lastName.length }' !</div>;
	}
}


ReactDOM.render(
	<App name="Damian" lastName="Raul" />,
	document.getElementById('root')
);
