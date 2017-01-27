import os

from libqtile.widget.base import ThreadedPollText


class TempSensor(ThreadedPollText):
    defaults = [
        ('update_interval', 10, ''),
        ('hwmon', '/sys/devices/platform/coretemp.0/hwmon/', ''),
        ('sensor_number', 1, ''),
    ]

    def __init__(self, **config):
        ThreadedPollText.__init__(self, **config)
        self.add_defaults(TempSensor.defaults)
        self.markup = True
        self.filename = None

    def get_filename(self):
        if os.path.exists(self.hwmon):
            ls = os.listdir(self.hwmon)
            if len(ls) == 0:
                return
            hwmon_dir = ls[0]

            return os.path.join(self.hwmon, hwmon_dir, "temp{}_".format(self.sensor_number))

    def get_param(self, name):
        if self.filename is None:
            self.filename = self.get_filename()

        try:
            with open(self.filename + name, 'r') as f:
                return int(f.read().strip()) / 1000
        except Exception:
            self.log.exception("Failed to get %s" % name)
            raise

    def poll(self):
        try:
            crit = self.get_param('crit')
            temp = self.get_param('input')
        except:
            return "TempError"

        if temp > 0.9 * crit:
            color = "red"
            icon = "\uf2c7"
        elif temp > 0.8 * crit:
            color = "orange"
            icon = "\uf2c8"
        elif temp > 0.7 * crit:
            color = None
            icon = "\uf2c9"
        elif temp > 0.6 * crit:
            color = None
            icon = "\uf2ca"
        else:
            color = None
            icon = "\uf2cb"

        if color:
            return '<span foreground="{}">{} {:.0f}\xb0C</span>'.format(color, icon, temp)

        return '{} {:.0f}\xb0C'.format(icon, temp)
