#!/usr/bin/python

import gobject

import dbus
import dbus.service
import dbus.mainloop.glib
import pygst
pygst.require('0.10')
import gst


class Player(object):
    def __init__(self, channel, error_handler):
        self.volume_level = 10
        self.error_handler = error_handler

        self.pipeline = gst.Pipeline("RadioPipe")
        self.player = gst.element_factory_make("playbin", "player")
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.__gst_message)

        self.pipeline.add(self.player)
        self.player.set_property('uri', channel)

    def play(self):
        self.pipeline.set_state(gst.STATE_PLAYING)

    def stop(self):
        self.pipeline.set_state(gst.STATE_PAUSED)

    def increase_volume(self):
        self.volume_level += 0.1
        self.__set_volume(self.volume_level)

    def decrease_volume(self):
        self.volume_level -= 0.1
        self.__set_volume(self.volume_level)

    def __set_volume(self, value):
        self.player.set_property('volume', float(value))

    def __gst_message(self, bus, message):
        if message.type == gst.MESSAGE_EOS or message.type == gst.MESSAGE_ERROR:
            self.error_handler()


class Radio(dbus.service.Object):

    def __init__(self, conn, object_path):
        super(Radio, self).__init__(conn, object_path)
        self.player = None

    @dbus.service.method("com.github.wjam.piclock.Radio", in_signature='s')
    def change_channel(self, new_channel):
        """Change the radio to the URL in the `new_channel`"""
        self.stop()
        self.player = Player(new_channel, self.play_emergency_noise)
        self.player.play()

    @dbus.service.method("com.github.wjam.piclock.Radio")
    def stop(self):
        if self.player is not None:
            self.player.stop()

    @dbus.service.method("com.github.wjam.piclock.Radio")
    def increase_volume(self):
        # TODO: This really distorts the sound for some reason
        if self.player is not None:
            self.player.increase_volume()

    @dbus.service.method("com.github.wjam.piclock.Radio")
    def decrease_volume(self):
        # TODO: This really distorts the sound for some reason
        if self.player is not None:
            self.player.decrease_volume()

    def play_emergency_noise(self):
        # TODO: Need to do something when we can't connect to the stream for some reason; maybe retry a number of times?
        print("Error")


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("com.github.wjam.piclock", session_bus)
    radio = Radio(session_bus, '/Radio')

    mainloop = gobject.MainLoop()
    mainloop.run()
