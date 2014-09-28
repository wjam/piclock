#!/usr/bin/python

import os
import json
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage

ETC_DIR = os.path.join(os.path.dirname(__file__), '../etc')
CONFIG = json.load(open(os.path.join(ETC_DIR, 'config.json'), 'r'))

storage = Storage(os.path.join(ETC_DIR, 'credentials.dat'))

credentials = storage.get()

http = httplib2.Http()
http = credentials.authorize(http)

service =\
    build(serviceName='calendar', version='v3', http=http, developerKey=CONFIG['developer_key'])

# print service.events().list(calendarId='will.j.may@gmail.com').execute()

for calendar_list_entry in service.calendarList().list().execute()['items']:
    print calendar_list_entry['summary']
