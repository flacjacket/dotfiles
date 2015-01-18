from icontextbox import IconTextBox

import cairocffi
import re
import subprocess

VOL_LOW = 30
VOL_HIGH = 80


def _stroke_speaker(ctx):
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(5)
    ctx.set_line_join(cairocffi.LINE_JOIN_ROUND)
    ctx.move_to(39.389, 26.769)
    ctx.line_to(22.235, 41.606)
    ctx.line_to(6, 41.606)
    ctx.line_to(6, 60.699)
    ctx.line_to(21.989, 60.699)
    ctx.line_to(39.389, 75.75)
    ctx.line_to(39.389, 26.769)
    ctx.close_path()
    ctx.stroke_preserve()
    ctx.fill()


def _stroke_mute(ctx):
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(5)
    ctx.set_line_cap(cairocffi.LINE_CAP_ROUND)
    ctx.move_to(48.651772, 63.269646)
    ctx.line_to(69.395223, 38.971024)
    ctx.stroke()
    ctx.move_to(69.395223, 63.269646)
    ctx.line_to(48.651772, 38.971024)
    ctx.stroke()


def _stroke_low(ctx):
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(5)
    ctx.set_line_cap(cairocffi.LINE_CAP_ROUND)
    ctx.move_to(48.128, 62.03)
    ctx.curve_to(50.057, 58.934, 51.19, 55.291, 51.19, 51.377)
    ctx.curve_to(51.19, 47.399, 50.026, 43.703, 48.043, 40.577)
    ctx.stroke()


def _stroke_medium(ctx):
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(5)
    ctx.set_line_cap(cairocffi.LINE_CAP_ROUND)
    ctx.move_to(55.082, 33.537)
    ctx.curve_to(58.777, 38.523, 60.966, 44.694, 60.966, 51.377)
    ctx.curve_to(60.966, 57.998, 58.815, 64.115, 55.178, 69.076)
    ctx.stroke()


def _stroke_high(ctx):
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(5)
    ctx.set_line_cap(cairocffi.LINE_CAP_ROUND)
    ctx.move_to(61.71, 75.611)
    ctx.curve_to(66.977, 68.945, 70.128, 60.531, 70.128, 51.378)
    ctx.curve_to(70.128, 42.161, 66.936, 33.696, 61.609, 27.01)
    ctx.stroke()

re_vol = re.compile('\[(\d?\d?\d?)%\]')


class Volume(IconTextBox):
    defaults = [
        ('update_interval', 1, 'The update interval'),
        ("cardid", 0, "Card Id"),
        ("channel", "Master", "Channel"),
        ("mute_command", None, "Mute command"),
        ("volume_up_command", None, "Volume up command"),
        ("volume_down_command", None, "Volume down command"),
    ]

    def __init__(self, **config):
        IconTextBox.__init__(self, **config)
        self.add_defaults(Volume.defaults)

        self.icon_size = 75, 100
        self.volume = None

    def get_volume(self):
        mixerprocess = subprocess.Popen(
            ['amixer', '-c', str(self.cardid), 'sget', self.channel],
            stdout=subprocess.PIPE
        )
        mixer_out = mixerprocess.communicate()[0].decode()
        if mixerprocess.returncode:
            return -1

        if '[off]' in mixer_out:
            return -1

        volgroups = re_vol.search(mixer_out)
        if volgroups:
            return int(volgroups.groups()[0])
        else:
            # this shouldn't happen
            return -1

    def poll(self):
        self.volume = self.get_volume()

        if self.volume <= 0:
            return [0], ""
        elif self.volume <= VOL_LOW:
            return [1], ""
        elif self.volume <= VOL_HIGH:
            return [2], ""
        else:
            return [3], ""

    def gen_icon(self, level, ctx):
        _stroke_speaker(ctx)

        if level == 0:
            _stroke_mute(ctx)

        if level >= 1:
            _stroke_low(ctx)
        if level >= 2:
            _stroke_medium(ctx)
        if level >= 3:
            _stroke_high(ctx)
