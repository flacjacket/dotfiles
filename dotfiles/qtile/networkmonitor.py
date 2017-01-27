from libqtile.widget.base import ThreadedPollText

from wifi import scan
from iwlib import get_iwconfig

import netifaces
import re



class NetworkMonitor(ThreadedPollText):

    defaults = [
        ("update_interval", 5, ""),
    ]

    def __init__(self, **config):
        ThreadedPollText.__init__(self, **config)
        self.add_defaults(NetworkMonitor.defaults)

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
                    return "\uf023"
                except (KeyError, IndexError):
                    pass
            return "\uf127"

        try:
            c = get_iwconfig(iface)
        except AttributeError:
            if iface[:3] == "usb":
                return "\uf287"
            else:
                return "\uf0e8"

        quality = c[b'stats'][b'quality']
        if quality >= 53:
            wifi_quality = 4
        elif quality >= 35:
            wifi_quality = 3
        elif quality >= 17:
            wifi_quality = 2
        else:
            wifi_quality = 1

        return "\uf1eb " + c[b'ESSID'].decode()

        # if c.encrypted and c.encryption_type != 'wep':
        #     pass
        # else:
        #     pass
