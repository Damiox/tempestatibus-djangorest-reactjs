## Introduction

This solution is using Django Rest Framework for the API server and ReactJS to work in the client framework and manage the DOM.
Users are able to subscribe to a Newsletter. The subscription process requires the User to confirm a link sent to his/her e-mail address.


Once the subscription is confirmed, this current solution requires to manually command the newsletter to be sent.


This is my first project with Django and ReactJS :)

## Requirements

You need to have Python3 and pip3 installed.
```
$ sudo apt install python3.5 pip
```


Additionally, you need to have sendmail installed and properly configured.
Please follow this guide for more information about how to configure sendmail: https://linuxconfig.org/configuring-gmail-as-sendmail-email-relay

## Getting Started

You create a virtual environment for this Python solution:
```
$ virtualenv env -p python3.5
```

Then you need to install the required dependencies on this virtual environment:
```
(env) $ source env/bin/activate
(env) $ pip install -r requirements.txt
```

Then, you need to set up the local database (sqlite) by running the following Django management commands:
```
(env) $ python manage.py makemigrations
(env) $ python manage.py migrate
(env) $ python manage.py loaddata --verbosity=2 tempestatibus/fixtures/top100uscities.json
```

## Setting the Configuration Variables

This solution requires the following configuration variables to be set:
* SECRET_KEY: referred to the key being used to generate internal hashes, among others. Set it to a random String.
* WUNDERGROUND_APIKEY: referred to the key obtained in the Wunderground API website (https://www.wunderground.com/weather/api/)
* API_URL (optional): it's the public URL for the API clients to use this API.

## Looking around the Database

This solution is using the sqlite database. You can login into the database by running the following command:
```
$ sqlite3 db.sqlite3
```
If you need help with the commands provided by sqlite, then you may want to enter `.help` in the sqlite console for better understanding.


The database has two tables defined as follows:

### Location

This table will contain the top 100 US Location by population based on the latest Census. This table will be initialized with the fixture that it is being specified in `top100uscities.json`
```
CREATE TABLE "api_location" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "city_name" varchar(100) NOT NULL, "population" integer NOT NULL);
```

### Subscription

This table will contain all the subscriptions and the ones that still need to be confirmed by the User. 
```
CREATE TABLE "api_subscription" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "email" varchar(254) NOT NULL, "confirmation_id" char(32) NOT NULL, "confirmation_requested_at" datetime NOT NULL, "subscribed" bool NOT NULL, "location_id" integer NOT NULL REFERENCES "api_location" ("id") DEFERRABLE INITIALLY DEFERRED, "subscribed_at" datetime NULL);
CREATE INDEX "api_subscription_location_id_5766f061" ON "api_subscription" ("location_id");
```

## Starting the Application

Run the Django server by running the following command:
```
(env) $  python manage.py runserver
```

Open up a browser and go to `http://localhost:8000/` and enjoy this application!

## Send Newsletter

Currently, this feature is being implemented by running a Django management command as detailed below:
```
$ python manage.py sendnewsletter
```

## Code Linting

There is a unit test (test_flake8_conformance) defined that will run `flake8` (http://flake8.pycqa.org/en/latest/user/index.html) to parse the solution code and look for mistakes. To use it simply run the following command from the solution directory:
```
$ python manage.py test
```

If flake8 detects any error then the details will be printed out.

## Web Client (ReactJS)

To build the client side, please execute the below command:
```
$ npm run build
```

This will run webpack which will build the React JS components.

If succeeded, then it will create a bundle file that will be located at: ./tempestatibus/static/bundles/bundle-[hash].js
At the same time, we have configured django-webpack-loader in settings.py in Django to track (through ./webpack-stats.json) when webpack creates a new bundle file, and automatically load it for testing.

### Structure

`index.js`: the solution is using React Router 4 to make an internal routing in client-side to the corresponding web component.
`util.js`: small utility to get a cookie value by name. It's being used to send the CSRF Token in the Ajax request.
`components/`: this folder contains all the React components being used for the solution.

### Notes when deploying to production

The `./tempestatibus/static` should be served by a known Web Server such as `nginx`, which is good for static content management and delivery, and then this Web Server should also act as a Web Proxy to interact with the Django REST API in a controlled local network. Django should listen to API requests into whatever TCP port in a local address accessible from the Web Proxy. The Web Proxy would be mapping `{hostname}/api/v1` to the Django REST API. Thus, this Web Server/Proxy would be the only component being exposed to the Internet.


## TODO
- Add logs
- Add better comments in the code
- Need some transaction layer when interacting with the database.
- Improved current functionality in `views.py`. Maybe to have 1 file per API.
- Review Webpack test server as I didn't use it.
- We should store State in another field in `api_location` table instead of parsing that field later

## Product Improvement
- Take into account Location's Timezone to send newsletter daily at the proper time.
- Review sendmail queueing functionality if the system grows.
- Beautify the HTML e-mail body.



