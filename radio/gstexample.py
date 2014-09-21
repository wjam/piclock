#!/usr/bin/python

import pygst
pygst.require('0.10')
import gst

import time

class Player(object):
    def __init__(self, channel):
        self.pipeline = gst.Pipeline("RadioPipe")
        self.player = gst.element_factory_make("playbin", "player")
        self.pipeline.add(self.player)
        self.player.set_property('uri', channel)

    def play(self):
        self.pipeline.set_state(gst.STATE_PLAYING)

    def stop(self):
        self.pipeline.set_state(gst.STATE_PAUSED)

# mms://wmlive-acl.bbc.net.uk/wms/bbc_ami/radio1/radio1_bb_live_ep1_sl0
player = Player("http://http-live.sr.se/p1-mp3-192")

while 1:
    command = raw_input("command\n")
    if command == "play":
        player.play()
    if command == "stop":
        player.stop()
    if command == "new":
        channel = raw_input("new radio channel")
        player.stop()
        player = Player(channel)
        player.play()
    if command == "exit":
        break
