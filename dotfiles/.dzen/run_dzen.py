#!/bin/env python

from __future__ import print_function

import os
import psutil
import subprocess
import sys
import threading
from ctypes import *
from time import localtime, strftime

dzen_cmd = "/usr/bin/dzen2 -xs 1 -ta r -h 13 -w 500 -x -500 -fn -*-terminus-*-r-normal-*-*-90-*-*-*-*-iso8859-* -p"
xkb_cmd = "/home/sean/.dzen/xkblayout print %e"
icon_dir = os.path.expanduser("~/.dzen/icons")
temp_file = "/sys/bus/platform/devices/coretemp.0/temp1_input"

dzen_thread = 0

# Dict that prints on update
class UpdatingDict(dict):
    def __init__(self, output, *args, **kwargs):
        self._output = output
        return dict.__init__(self, *args, **kwargs)

    def __setitem__(self, key, value):
        printing = False
        if key not in self or self[key] != value:
            dict.__setitem__(self, key, value)
            vals = ["^fg(white)" + self[i] + "^fg()" for i in sorted(self.keys())]
            print(" | ".join(vals) + "  ", file=self._output)
        else:
            dict.__setitem__(self, key, value)

# Delaying wrapper
def withdelay(sec):
    def wrapper(func):
        def delayed_func(*args, **kwargs):
            func(*args, **kwargs)
            threading.Timer(sec, delayed_func, args, kwargs).start()
        return delayed_func
    return wrapper

# Dict updating wrapper
def updatedict(key):
    def wrapper(func):
        def call_and_save(d, *args, **kwargs):
            d[key] = func(*args, **kwargs)
        return call_and_save
    return wrapper

def get_icon(filename):
    return "^i(%s)" % os.path.join(icon_dir, filename)

import dbus
bus = dbus.SystemBus()
from netifaces import interfaces, AF_INET, ifaddresses
@withdelay(10)
@updatedict(10)
def set_network():
    p = bus.get_object("org.wicd.daemon", '/org/wicd/daemon')
    daemon = dbus.Interface(p, 'org.wicd.daemon')
    conn = str(daemon.GetCurrentInterface())

    if conn == '':
        return ""

    iface = conn[:-1]
    net_info = ""
    if iface == 'wlan':
        p = bus.get_object("org.wicd.daemon", '/org/wicd/daemon/wireless')
        wireless = dbus.Interface(p, 'org.wicd.daemon.wireless')

        network_id = wireless.GetCurrentNetworkID(0)
        ssid = wireless.GetWirelessProperty(network_id, "essid")
        #rate = wireless.GetWirelessProperty(network_id, "bitrates")
        #signal = wireless.GetWirelessProperty(network_id, "strength")
        if wireless.GetWirelessProperty(network_id, "encryption"):
            net_info = get_icon("lock.xbm") + "^p(3)"

        net_info += get_icon("net_wifi.xbm") + "^p(5)"
        net_info += "%s" % ssid
    elif iface == 'eth':
        net_info = get_icon("net_wired.xbm")
    elif iface == 'usb':
        net_info = get_icon("net_usb.xbm")

    conn = [i for i in interfaces() if i != 'lo' and AF_INET in ifaddresses(i)]
    if 'ppp0' in conn:
        net_info += "^p(3)" + get_icon("key.xbm")

    return net_info

@withdelay(5)
@updatedict(30)
def set_bat():
    with open('/sys/class/power_supply/AC/online') as f:
        ac_power = f.read() == '1\n'
    with open('/sys/class/power_supply/BAT0/status') as f:
        bat_charging = f.read() == 'Charging\n'

    if ac_power and not bat_charging:
        return get_icon("ac.xbm")

    with open('/sys/class/power_supply/BAT0/capacity') as f:
        bat_charge = int(f.read())
    bat_icon = "battery%d.xbm" % ((bat_charge // 10) * 10)

    if ac_power:
        return "%s %s %d%%" % (get_icon("ac.xbm"), get_icon(bat_icon), bat_charge)
    return "%s %d%%" % (get_icon(bat_icon), bat_charge)

@withdelay(2)
@updatedict(80)
def set_xkb():
    p = subprocess.Popen(xkb_cmd.split(), stdout=subprocess.PIPE)
    layout = p.stdout.read().strip()
    return "%s" % layout

@withdelay(5)
@updatedict(90)
def set_hdw():
    cpu = psutil.cpu_percent()
    cpu = "%s^p(3)%2d%%" % (get_icon("cpu.xbm"), cpu)

    mem = psutil.virtual_memory().percent
    mem = "%s^p(3)%2d%%" % (get_icon("mem.xbm"), mem)

    with open(temp_file, 'r') as f:
        temp = int(f.read().strip())
    temp = "%s^p(3)%2dC" % (get_icon("temp.xbm"), temp // 1000)

    return "%s %s %s" % (cpu, mem, temp)

@withdelay(1)
@updatedict(100)
def set_date():
    return strftime("%a %b %d %Y %H:%M:%S", localtime())

def get_disp():
    import xrandr
    screen = xrandr.get_current_screen()
    outputs = []
    for n, o in screen.outputs.items():
        if o.is_connected():
            o.set_to_prefered_mode()
            outputs.append(o)
        else:
            o.disable()
    outputs = sorted(outputs, key=lambda o: o.id)
    for l, r in zip(outputs[:-1], outputs[1:]):
        l.set_relation(r, xrandr.RELATION_LEFT_OF)
    screen.apply_output_config()
    return scrs

def main():
    global dzen_thread
    fn = os.path.expanduser('~/.dzen/pid')

    #screens = get_disp()

    dzen_thread = subprocess.Popen(dzen_cmd.split(), stdin=subprocess.PIPE)
    output = UpdatingDict(dzen_thread.stdin)
    with open(fn, 'w') as f:
        f.write(str(dzen_thread.pid))
        f.write('\n')
        f.write(str(os.getpid()))
        f.write('\n')

    # 10
    set_network(output)
    # 30
    set_bat(output)
    # 80
    set_xkb(output)
    # 90
    set_hdw(output)
    # 100
    set_date(output)
    # 110
    #set_volume(output)

if __name__ == '__main__':
    main()
