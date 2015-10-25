from networkmonitor_icons import wired_icon, wifi_icon, noconn_icon, vpn_icon

from enum import Enum
from icontextbox import IconTextBox
from wifi import scan

import netifaces
import re


vpn_iface = 'tun0'

Iface = Enum('Iface', 'no_conn wired wifi vpn')



class NetworkMonitor(IconTextBox):
    def __init__(self, **config):
        IconTextBox.__init__(self, **config)
        self.iface = Iface.no_conn

    @property
    def icon_size(self):
        if self.iface in (Iface.wifi, Iface.no_conn):
            return 2048, 2500
        elif self.iface == Iface.wired:
            return 430, 400
        else:
            return 0, 0

    def poll(self):
        gws = netifaces.gateways()
        try:
            iface = gws['default'][netifaces.AF_INET][1]
        except (IndexError, KeyError):
            self.iface = Iface.no_conn
            return [[Iface.no_conn]], ''

        try:
            c = list(scan.Cell.all(iface))[0]
        except (scan.InterfaceError, FileNotFoundError):
            self.iface = Iface.wired
            gen_icon = [Iface.wired, ]
        else:
            quality = int(re.match(r"(\d+)/\d+", c.quality).group(1))
            if quality >= 53:
                wifi_quality = 4
            elif quality >= 35:
                wifi_quality = 3
            elif quality >= 17:
                wifi_quality = 2
            else:
                wifi_quality = 1

            # if c.encrypted and c.encryption_type != 'wep':
            #     pass
            # else:
            #     pass

            self.iface = Iface.wifi
            gen_icon = [Iface.wifi, wifi_quality]

        try:
            if netifaces.AF_INET in netifaces.ifaddresses(vpn_iface):
                gen_icon.append(Iface.vpn)
        except ValueError:
            pass

        return [gen_icon], ''

    def gen_icon(self, value, ctx):
        try:
            iface = value[0]
        except IndexError:
            return

        if value[-1] == Iface.vpn:
            vpn_icon(ctx)
            # ctx.set_source_rgba(0, 0, 0, 0)
            # x, y = self.icon_size
            # ctx.move_to(x, y)
            # ctx.rectangle(0, 0, x, y)
            # ctx.rectangle(0, 0, x, y/2)
            # ctx.clip()
            # ctx.new_path()
        elif iface == Iface.wired:
            wired_icon(ctx)
        elif iface == Iface.wifi:
            quality = value[1]
            wifi_icon(ctx, quality)
        else:
            noconn_icon(ctx)
