import os

from libqtile.widget.base import ThreadedPollText


BAT_DIR = '/sys/class/power_supply'

BATTERY_INFO_FILES = {
    'energy_now_file': ['energy_now', 'charge_now'],
    'energy_full_file': ['energy_full', 'charge_full'],
    'power_now_file': ['power_now', 'current_now'],
    'status_file': ['status'],
}


class Battery(ThreadedPollText):
    defaults = [
        ('update_interval', 10, ''),
        ('battery_name', 'BAT0', 'ACPI name of a battery, usually BAT0'),
        ('status_file', 'status', 'Name of status file in /sys/class/power_supply/battery_name'),
    ]

    def __init__(self, **config):
        ThreadedPollText.__init__(self, **config)
        self.add_defaults(Battery.defaults)
        self.markup = True

        self.filenames = {}

    def load_file(self, name):
        try:
            path = os.path.join(BAT_DIR, self.battery_name, name)
            with open(path, 'r') as f:
                return f.read().strip()
        except IOError:
            if name == 'current_now':
                return 0
            return False
        except Exception:
            self.log.exception("Failed to get %s" % name)

    def get_param(self, name):
        if name in self.filenames:
            if self.filenames[name]:
                return self.load_file(self.filenames[name])
        else:
            # Don't have the file name cached, figure it out

            # Don't modify the global list! Copy with [:]
            file_list = BATTERY_INFO_FILES.get(name, [])[:]

            if getattr(self, name, None):
                # If a file is manually specified, check it first
                file_list.insert(0, getattr(self, name))

            # Iterate over the possibilities, and return the first valid value
            for file in file_list:
                value = self.load_file(file)
                if not (value in (False, None)):
                    self.filenames[name] = file
                    return value

            # If we made it this far, we don't have a valid file.
            # Set it to None to avoid trying the next time.
            self.filenames[name] = None

            return None

    def poll(self):
        try:
            info = {
                'stat': self.get_param('status_file'),
                'now': float(self.get_param('energy_now_file')),
                'full': float(self.get_param('energy_full_file')),
                'power': float(self.get_param('power_now_file')),
            }
        except TypeError:
            return 'BatteryError'

        charging = info['stat'] == "Charging"
        discharging = info['stat'] == "Discharging"

        # we are fully charged
        if not (discharging or charging):
            return ''

        percent = info['now'] / info['full']

        if charging:
            return "\uf1e6 {:.0%}".format(percent)

        if percent > .8:
            icon = "\uf240"
        elif percent > .6:
            icon = "\uf241"
        elif percent > .4:
            icon = "\uf242"
        elif percent > .2:
            icon = '\uf243'
        else:
            icon = '<span foreground="red">\uf244</span>'

        return "{} {:.0%}".format(icon, percent)
