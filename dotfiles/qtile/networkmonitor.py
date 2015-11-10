from networkmonitor_icons import wired_icon, wifi_icon, noconn_icon, vpn_icon, usb_icon

from enum import Enum
from icontextbox import IconTextBox
from wifi import scan

import netifaces
import re


Iface = Enum('Iface', 'no_conn wired wifi vpn usb')
usb_iface = 'usb'


class NetworkMonitor(IconTextBox):
    def __init__(self, **config):
        IconTextBox.__init__(self, **config)
        self.iface = Iface.no_conn

    @property
    def icon_size(self):
        if self.iface in (Iface.wifi, Iface.no_conn, Iface.vpn):
            return 2048, 2500
        elif self.iface == Iface.wired:
            return 430, 400
        elif self.iface == Iface.usb:
            return 355, 275
        else:
            return 0, 0

    def poll(self):
        gws = netifaces.gateways()

        try:
            # Try to figure out if we're connected normally
            iface = gws['default'][netifaces.AF_INET][1]
        except (IndexError, KeyError):
            # We might be on a VPN
            for iface in netifaces.interfaces():
                if iface == 'lo':
                    continue
                adr = netifaces.ifaddresses(iface)
                try:
                    adr[netifaces.AF_INET][0]['peer']
                    self.iface = Iface.vpn
                    return [[Iface.vpn]], iface
                except (KeyError, IndexError):
                    pass

            self.iface = Iface.no_conn
            return [[Iface.no_conn]], ''

        text = ''
        try:
            c = list(scan.Cell.all(iface))[0]
        except (scan.InterfaceError, FileNotFoundError):
            if iface[:3] == usb_iface:
                self.iface = Iface.usb
            else:
                self.iface = Iface.wired
            gen_icon = [self.iface]
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
            text = c.ssid

            # if c.encrypted and c.encryption_type != 'wep':
            #     pass
            # else:
            #     pass

            self.iface = Iface.wifi
            gen_icon = [Iface.wifi, wifi_quality]

        return [gen_icon], text

    def gen_icon(self, value, ctx):
        try:
            iface = value[0]
        except IndexError:
            return

        if value[-1] == Iface.vpn:
            vpn_icon(ctx)
        elif iface == Iface.wired:
            wired_icon(ctx)
        elif iface == Iface.wifi:
            quality = value[1]
            wifi_icon(ctx, quality)
        elif iface == Iface.usb:
            usb_icon(ctx)
        else:
            noconn_icon(ctx)
