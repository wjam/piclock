##Notes on initial setup of the Raspberry Pi##

##Layout of the application##

###Radio script###
Responsible for playing music from an internet stream

* Use gstreamer to play an external URL
* Use DBus to listen for messages
    * Listen for message to shutdown (Unix way would be to have a PID file)
    * Listen for messages to change volume
    * Listen for messages to change channel (?)
    * http://cgit.freedesktop.org/dbus/dbus-python/tree/examples/example-client.py
    * http://cgit.freedesktop.org/dbus/dbus-python/tree/examples/example-service.py
* Is this script a daemon or does it kill itself when the radio is not playing?

###Alarm script###
Responsible for kicking off the radio script. This is what the cron script will call.

###Alarm management script###
Responsible for maintaining the crontab which will kick start the alarm script.

* Run via cron, probably run multiple times a day (once an hour?)
* Connects to Google Calendar to retrieve changes to the alarm clock events.
    * https://developers.google.com/google-apps/calendar/
* Adds new alarm clock events for the next x weeks.
    * Will need to record what date the application is up to
        * Where will this information be stored? GConf? /etc?
* Calendar event should have radio station on it

###LCD script###
Responsible for managing the LCD screen and also the buttons around the LCD.

* http://www.adafruit.com/products/1110
* Should the management of the buttons be in this script or a separate one?
* Adafruit custom code or LCDproc?
    * Does Adafruit support LCDproc? (probably not for that product)
* Regularly updates LCD - possibly have to update the time as well?
* Listens to button presses, through i2c, and emits DBus messages to the radio
* 6 buttons available:
    * Switch radio on/off
    * Volume up
    * Volume down
    * Channel up
    * Channel down
    * ???

###Web front end###
* Manages list of radio stations to URLs
* Handles the Google authentication
* Alter Calendar details(?)
* Probably not written in Java 8 due to memory/speed issues
* Python/Bootstrap/AnuglarJS application which minimises what the Pi actually needs to serve
    * http://flask.pocoo.org/
    * http://mattrichardson.com/Raspberry-Pi-Flask/
    * http://flaskpi.com/

##Tools required##
* Soldering Iron
* Solder sucker
