#!/usr/bin/python

import os
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage

ETC_DIR = os.path.join(os.path.dirname(__file__), '..')

# To disable the local server feature, uncomment the following line:
# FLAGS.auth_local_webserver = False

storage = Storage(os.path.join(ETC_DIR, 'credentials.dat'))

credentials = storage.get()

http = httplib2.Http()
http = credentials.authorize(http)

service =\
    build(serviceName='calendar', version='v3', http=http, developerKey='65009c1094cdb2dc8c0cc601dd18ac61e173e688')

# print service.events().list(calendarId='will.j.may@gmail.com').execute()

for calendar_list_entry in service.calendarList().list().execute()['items']:
    print calendar_list_entry['summary']
