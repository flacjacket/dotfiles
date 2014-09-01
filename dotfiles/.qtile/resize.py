#!/bin/env python

import re
import subprocess

def resize(primary=None, primary_mode=None,
        secondary=None, secondary_mode=None, secondary_location="--right-of",
        toggle=False, clone=False):
    screeninfo = subprocess.check_output(['xrandr', '-d', ':0.0']).decode()
    screens = sorted(re.findall("(\w+) connected", screeninfo))

    # this is an odd case...
    if len(screens) == 0:
        return

    enabled_screens = len(re.findall("(\*)", screeninfo))
    unplugged_screens = re.findall("(\w+) disconnected \d+x\d+", screeninfo)

    # Determine primary display
    # If not explicitly passed
    if not primary or primary not in screens:
        if "LVDS1" in screens:
            # None specified, use LVDS1
            primary = "LVDS1"
        else:
            # odd case...
            primary = screens[0]
    screens.pop(screens.index(primary))

    # Determine secondary display
    if (toggle and enabled_screens > 1) or len(screens) == 0:
        # If multiple are enabled, toggle to only main screen
        secondary = None
    else:
        # If not explicitly passed
        if not secondary and secondary not in screens:
            secondary = screens[0]
            screens.pop(screens.index(secondary))

    if (clone or toggle) and secondary:
        # Get the modes available to both screens
        mode_list = re.split("(\w+) (?:dis)?connected.*?\n", screeninfo)[1:]
        primary_modes = set(re.findall('(\d+x\d+)', mode_list[mode_list.index(primary) + 1]))
        secondary_modes = set(re.findall('(\d+x\d+)', mode_list[mode_list.index(secondary) + 1]))

        # Shared modes
        modes = primary_modes.intersection(secondary_modes)
        if modes:
            modes = sorted(modes, key=lambda item: [-int(res) for res in re.findall('\d+', item)])
            primary_mode = secondary_mode = modes[0]
            secondary_location = '--same-as'

    disable_screens = screens + unplugged_screens

    command = "xrandr --output %s --primary" % primary
    if primary_mode:
        command += " --mode %s" % primary_mode
    else:
        command += " --auto"

    if secondary:
        command += " --output %s" % secondary
        command += " %s %s" % (secondary_location, primary)
        if secondary_mode:
            command += " --mode %s" % secondary_mode
        else:
            command += " --auto"

    for s in disable_screens:
        command += " --output %s --off" % s

    subprocess.call(command.split())

if __name__ == '__main__':
    resize()
