#!/usr/bin/python

import dbus


def main():
    bus = dbus.SessionBus()

    remote_clock = dbus.Interface(bus.get_object("com.github.wjam.piclock", "/Radio"),
                                  "com.github.wjam.piclock.Radio")

    remote_clock.change_channel("mms://wmlive-acl.bbc.net.uk/wms/bbc_ami/radio1/radio1_bb_live_ep1_sl0")
    #remote_clock.increase_volume()
    #remote_clock.decrease_volume()
    #remote_clock.stop()

if __name__ == '__main__':
    main()
