#!/usr/bin/python

import os
import json
import httplib2
import pytz

from apiclient.discovery import build
from oauth2client.file import Storage
from datetime import datetime, timedelta
from crontab import CronTab

ETC_DIR = os.path.join(os.path.dirname(__file__), '../etc')
CONFIG = json.load(open(os.path.join(ETC_DIR, 'config.json'), 'r'))

cron_tab = CronTab(user=True)


class AlarmEvent:

    def __init__(self, alarm_time, radio_station, source):
        self._alarm_time = alarm_time
        self._radio_station = radio_station
        self._source = source

    def alarm_time(self):
        return self._alarm_time

    def matches(self, other):
        return self.alarm_time == other.alarm_time


def get_events_from_google():

    storage = Storage(os.path.join(ETC_DIR, 'credentials.dat'))

    credentials = storage.get()

    http = httplib2.Http()
    http = credentials.authorize(http)

    service = \
        build(serviceName='calendar', version='v3', http=http, developerKey=CONFIG['developer_key'])

    start = datetime.now(pytz.utc).replace(microsecond=0)
    to = (datetime.now(pytz.utc) + timedelta(days=7)).replace(microsecond=0)
    print to.isoformat()
    return \
        service.events().list(calendarId=CONFIG['calendar'], timeMin=start.isoformat(),
                              timeMax=to.isoformat()).execute()['items']


def alarm_events_from_google():
    # TODO probably need to parse the dateTime into a datetime
    return [AlarmEvent(event['start']['dateTime'], event['description'], event)
            for event in get_events_from_google()]


def get_events_from_cron():
    # TODO match job comment
    return [cron_job for cron_job in cron_tab if cron_job.comment == '']


def alarm_events_from_cron():
    # TODO extract station from job comment
    return [AlarmEvent(job.schedule(date_from=datetime.now()).get_next(), job.comment, job)
            for job in get_events_from_cron()]


# for event in get_events_from_google():
#     print event['summary'] + event['description'] + event['status'] + event['start']['dateTime'] +\
#         event['end']['dateTime']

cron_events = alarm_events_from_cron()
google_events = alarm_events_from_google()


def get_cron_event(google_event_to_match):
    for cron in cron_events:
        if cron.matches(google_event_to_match):
            return cron
    return None

# Update and remove any alarm events deleted from google
for google in google_events:
    cron_event = get_cron_event(google)
    if cron_event is not None:
        # Found an event; update it and then remove it from further consideration
        # TODO check that the cron_event is up to date (radio, command)
        cron_events.remove(cron_event)
    else:
        # No corresponding event found; add a new one
        new_job = cron_tab.new(command='', comment='')
        new_job.enable()
        new_job.setall()  # minutes, hours, day of month, month, None

# Remove any remaining cron events
[cron_tab.remove(e) for e in cron_events]

# TODO: take all of the google events, add one week to them and add them to google
