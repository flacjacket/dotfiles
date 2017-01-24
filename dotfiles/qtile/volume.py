from libqtile.widget.base import ThreadedPollText

import re
import shlex
import subprocess

VOL_LOW = 40
VOL_HIGH = 80


re_vol = re.compile('\[(\d?\d?\d?)%\]')

getvol_cmd = "amixer -c {cardid} sget {channel}"
voltoggle_cmd = "amixer -c {cardid} -q sset {channel} toggle"
volup_cmd = "amixer -c {cardid} -q sset {channel} {increment}%+"
voldown_cmd = "amixer -c {cardid} -q sset {channel} {increment}%-"


class Volume(ThreadedPollText):
    defaults = [
        ('update_interval', 3, 'The update interval'),
        ("cardid", 0, "Card Id"),
        ("channel", "Master", "Channel"),
        ("vol_increment", 4, "Percent to change the volume"),
    ]

    def __init__(self, **config):
        ThreadedPollText.__init__(self, **config)
        self.add_defaults(Volume.defaults)

        self.markup = True
        self.volume = None
        self.muted = None
        self.is_new_volume = False

        self.clear_new = None

    def get_volume(self):
        cmd = self.format_cmd(getvol_cmd)
        mixerprocess = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
        mixer_out = mixerprocess.communicate()[0].decode()

        if mixerprocess.returncode:
            return None

        if '[off]' in mixer_out:
            return -1

        volgroups = re_vol.search(mixer_out)
        if volgroups:
            return int(volgroups.groups()[0])
        else:
            # this shouldn't happen
            return None

    def poll(self):
        next_volume = self.get_volume()

        if next_volume is None:
            return "VolumeError "

        if self.volume is not None and (next_volume != self.volume):
            if self.clear_new is not None:
                self.clear_new.cancel()

            self.is_new_volume = True

            def clear_it(w):
                w.is_new_volume = False
                w.tick()
            self.clear_new = self.qtile.call_later(3, clear_it, self)

        self.volume = next_volume

        muted = self.volume < 0

        if muted:
            return '<big>\U0001f507</big>'
        elif self.volume <= VOL_LOW:
            icon = '<big>\uf026</big> '
        elif self.volume <= VOL_HIGH:
            icon = '<big>\uf027</big> '
        else:
            icon = '<big>\uf028</big> '

        if self.is_new_volume:
            return icon + " {:d}".format(self.volume)

        return icon

    def button_press(self, x, y, button):
        if button == 1:
            self.cmd_toggle()
        elif button == 4:
            self.cmd_volume_up()
        elif button == 5:
            self.cmd_volume_down()

    def cmd_toggle(self):
        cmd = self.format_cmd(voltoggle_cmd)
        process = subprocess.call(shlex.split(cmd))

        self.tick()

    def cmd_volume_up(self):
        cmd = self.format_cmd(volup_cmd, increment=self.vol_increment)
        process = subprocess.call(shlex.split(cmd))

        self.tick()

    def cmd_volume_down(self):
        cmd = self.format_cmd(voldown_cmd, increment=self.vol_increment)
        process = subprocess.call(shlex.split(cmd))

        self.tick()

    def format_cmd(self, cmd, **kwargs):
        return cmd.format(
            cardid=self.cardid,
            channel=self.channel,
            **kwargs
        )
