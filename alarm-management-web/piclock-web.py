#!/usr/bin/python

from flask import Flask, render_template
import httplib2
import flask
import json
import os

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow

ETC_DIR = os.path.join(os.path.dirname(__file__), '../etc')

CONFIG = json.load(open(os.path.join(ETC_DIR, 'config.json'), 'r'))

FLOW = OAuth2WebServerFlow(
    client_id=CONFIG['client_id'],
    client_secret=CONFIG['client_secret'],
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='pi-clock/1.0',
    response_type='code',
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
)

CREDENTIALS_STORE = Storage(os.path.join(ETC_DIR, 'credentials.dat'))

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template('main.html')

@app.route("/authorise", methods=['GET', 'POST'])
def authorise():
    if flask.request.method == 'GET':
        template_data = {
            'url': FLOW.step1_get_authorize_url(),
            'redirect_to': flask.request.args['to']
        }
        return render_template('auth.html', **template_data)

    # post back
    credentials = FLOW.step2_exchange(flask.request.form['code'])

    CREDENTIALS_STORE.put(credentials)

    return flask.redirect(flask.url_for(flask.request.form['to']))

@app.route("/select_calendar")
def select_calendar():

    credentials = CREDENTIALS_STORE.get()
    if credentials is None or credentials.invalid is True:
        return flask.redirect(flask.url_for('authorise', to='select_calendar'))

    http = credentials.authorize(httplib2.Http())

    service = \
        build(serviceName='calendar', version='v3', http=http, developerKey=CONFIG['developer_key'])

    calendars = service.calendarList().list().execute()

    template_data = {
        'calendars': [(c['id'], c['summary']) for c in calendars['items']]
    }
    return render_template('calendars.html', **template_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

# TODO
# configure list of radio stations
# manage Google authentication
# selection/creation of calendar
