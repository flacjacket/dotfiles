import cairocffi
import os

from icontextbox import IconTextBox


BAT_DIR = '/sys/class/power_supply'
CHARGED = 'Full'
CHARGING = 'Charging'
DISCHARGING = 'Discharging'
UNKNOWN = 'Unknown'

BATTERY_INFO_FILES = {
    'energy_now_file': ['energy_now', 'charge_now'],
    'energy_full_file': ['energy_full', 'charge_full'],
    'power_now_file': ['power_now', 'current_now'],
    'status_file': ['status'],
}


def _stroke_battery(ctx):
    # M469.9,192
    ctx.move_to(469.9, 192)
    # H433
    _, y = ctx.get_current_point()
    ctx.line_to(433, y)
    # v-54
    ctx.rel_line_to(0, -54)
    # c0-5.5-4.3-10-9.9-10
    ctx.rel_curve_to(0, -5.5, -4.3, -10, -9.9, -10)
    # H42.1
    _, y = ctx.get_current_point()
    ctx.line_to(42.1, y)
    # c-5.6,0-10.1,4.5-10.1,10
    ctx.rel_curve_to(-5.6, 0, -10.1, 4.5, -10.1, 10)
    # v236
    ctx.rel_line_to(0, 236)
    # c0,5.5,4.5,10,10.1,10
    ctx.rel_curve_to(0, 5.5, 4.5, 10, 10.1, 10)
    # h381.1
    ctx.rel_line_to(381.1, 0)
    # c5.5,0,9.9-4.5,9.9-10
    ctx.rel_curve_to(5.5, 0, 9.9, -4.5, 9.9, -10)
    # v-54
    ctx.rel_line_to(0, -54)
    # h36.9
    ctx.rel_line_to(36.9, 0)
    # c5.6,0,10.1-4.5,10.1-10
    ctx.rel_curve_to(5.6, 0, 10.1, -4.5, 10.1, -10)
    # V202
    x, _ = ctx.get_current_point()
    ctx.line_to(x, 202)
    # C480,196.5,475.5,192,469.9,192
    ctx.curve_to(480, 196.5, 475.5, 192, 469.9, 192)
    # z
    ctx.close_path()


def _stroke_value(ctx, value):
    mv = 337 * (20 - value) / 20
    # M401,160
    ctx.move_to(401, 160)
    # v64
    ctx.rel_line_to(0, 64)
    # H448
    _, y = ctx.get_current_point()
    ctx.line_to(448, y)
    # v64
    ctx.rel_line_to(0, 64)
    # H401
    _, y = ctx.get_current_point()
    ctx.line_to(401, y)
    # v64
    ctx.rel_line_to(0, 64)
    # move val
    ctx.rel_line_to(-mv, 0)
    # h-192
    ctx.rel_line_to(0, -192)
    # move val
    ctx.rel_line_to(mv, 0)
    # z
    ctx.close_path()


def _stroke_charging(ctx):
    # M257.4,160
    ctx.move_to(257.4, 160)
    # l-27.9,81
    ctx.rel_line_to(-27.8, 81)
    # H291
    _, y = ctx.get_current_point()
    ctx.line_to(291, y)
    # L190.6,352
    ctx.line_to(190.6, 352)
    # l27.9-81
    ctx.rel_line_to(127.9, -81)
    # H157
    _, y = ctx.get_current_point()
    ctx.line_to(157, y)
    # L257.4,160
    ctx.line_to(257.4, 160)
    # z
    ctx.close_path()


class Battery(IconTextBox):
    defaults = [
        ('battery_name', 'BAT0', 'ACPI name of a battery, usually BAT0'),
        ('status_file', 'status', 'Name of status file in /sys/class/power_supply/battery_name'),
    ]

    def __init__(self, **config):
        IconTextBox.__init__(self, **config)
        self.add_defaults(Battery.defaults)

        self.filenames = {}
        self.icon_size = (512, 512)

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
        if name in self.filenames and self.filenames[name]:
            return self.load_file(self.filenames[name])
        elif name not in self.filenames:
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
            return ([], 'Error')

        if info['stat'] in (DISCHARGING, CHARGING):
            percent = 100 * info['now'] // info['full']
            text = "%d%%" % percent

            return [(int(round(percent / 5)), info['stat'])], text
        else:
            return [], ''

    def gen_icon(self, value, ctx):
        # src: battery remaining /20
        prct, stat = value

        if prct <= 3 and stat == DISCHARGING:
            ctx.set_source_rgb(1, 0, 0)
        else:
            ctx.set_source_rgb(1, 1, 1)

        _stroke_battery(ctx)

        if prct < 20:
            _stroke_value(ctx, prct)
            ctx.fill()
            ctx.set_source_rgb(0.3, 0.3, 0.3)
            _stroke_value(ctx, prct)
        ctx.fill()

        if stat == CHARGING:
            ctx.set_source_rgb(0, 0, 0)
            _stroke_charging(ctx)
            ctx.fill()

