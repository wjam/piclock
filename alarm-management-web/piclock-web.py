#!/usr/bin/python

from flask import Flask, render_template
import httplib2
import flask
import json
import os

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow

ETC_DIR = os.path.join(os.path.dirname(__file__), '..')

CONFIG = json.load(open(os.path.join(ETC_DIR, 'config.json'), 'r'))

FLOW = OAuth2WebServerFlow(
    client_id=CONFIG['client_id'],
    client_secret=CONFIG['client_secret'],
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='pi-clock/1.0',
    redirect_uri=CONFIG['redirect_uri']
)

CREDENTIALS_STORE = Storage(os.path.join(ETC_DIR, 'credentials.dat'))

app = Flask(__name__)

@app.route("/")
def main_page():
    credentials = CREDENTIALS_STORE.get()
    if credentials is None or credentials.invalid is True:
        return flask.redirect(FLOW.step1_get_authorize_url())

    return flask.redirect(flask.url_for('select_calendar'))

@app.route("/oauth_callback")
def oauth_callback():
    if flask.request.args.get('error') is not None:
        return "problem occurred " + flask.request.args.get('error')

    credentials = FLOW.step2_exchange(flask.request.args.get('code'))

    CREDENTIALS_STORE.put(credentials)

    return flask.redirect(flask.url_for('select_calendar'))

@app.route("/select_calendar")
def select_calendar():

    credentials = CREDENTIALS_STORE.get()

    http = credentials.authorize(httplib2.Http())

    service = \
        build(serviceName='calendar', version='v3', http=http, developerKey=CONFIG['developer_key'])

    calendars = service.calendarList().list().execute()

    template_data = {
        'calendars': [c['summary'] for c in calendars['items']]
    }
    return render_template('calendars.html', **template_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

# TODO
# should change to the installed application type to avoid having to have IP address in application config.
# Will mean having to tweak the login/authentication part to have iframe

# configure list of radio stations
# manage Google authentication
# selection/creation of calendar