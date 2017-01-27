import os
import socket

from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile.dgroups import simple_key_binder
from libqtile import layout, bar, widget, hook

from resize import resize
import battery
import networkmonitor
import volume
import tempsensor

from subprocess import call

float_name = ('MPlayer',)
float_class = ('Xephyr', 'Weston Compositor', 'BLHeliSuite.exe', 'MW_OSD_GUI', 'yubikey-personalization-gui')

@hook.subscribe.startup_once
def start_once():
    resize()
    #call(['xsetroot', '-cursor_name', 'left_ptr'])
    #call(['dropbox'])


@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    call(['feh', '--bg-max', '/home/sean/.apod/apod.png'])
    qtile.cmd_restart()


@hook.subscribe.client_new
def dialogs(window):
    if window.window.get_name() in float_name or set(float_class).intersection(set(window.window.get_wm_class())) or window.window.get_wm_transient_for():
        window.floating = True


@hook.subscribe.startup
def startup_calls():
    call(['feh', '--bg-max', '/home/sean/.apod/apod.png'])


mod = "mod4"
alt = "mod1"

keys = [
    # Switch between windows in current stack pane
    Key([mod], "h", lazy.layout.down()),
    Key([mod], "t", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "shift"], "h", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "t", lazy.layout.shuffle_up()),

    # Change size of panels
    Key([mod], "m", lazy.layout.grow()),
    Key([mod], "b", lazy.layout.shrink()),
    Key([mod], "s", lazy.layout.normalize()),

    # Swap side of main monad pane
    Key([mod], "space", lazy.layout.flip()),

    # Move to left and right screens
    Key([mod], "d", lazy.to_screen(0)),
    Key([mod], "n", lazy.to_screen(1)),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.nextlayout()),
    Key([mod, "shift"], "w", lazy.window.kill()),

    # Toggle floating windows
    Key([mod], "f", lazy.window.toggle_floating()),

    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    # Applications
    Key([mod], "c", lazy.spawn("firefox")),
    Key([mod], "l", lazy.spawn("clementine")),
    Key([mod], "Return", lazy.spawn("alacritty")),
    # Key([mod], "i", lazy.spawn("ipython qtconsole --profile labwork")),
    Key([mod], "i", lazy.spawn("jupyter qtconsole")),
    Key([mod, "shift"], "l", lazy.spawn("xscreensaver-command -lock")),
    Key([], "Print", lazy.spawn("scrot")),

    # Multimedia keys
    Key([], "XF86Display", lazy.function(lambda q: resize(toggle=True))),
    Key([mod], "s", lazy.function(lambda q: resize())),
    Key([mod, "shift"], "s", lazy.function(lambda q: resize(clone=True))),
    Key([], "XF86AudioPlay", lazy.spawn("clementine --play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("clementine --next")),
    Key([], "XF86AudioPrev", lazy.spawn("clementine --prev")),
    Key([], "XF86AudioMute", lazy.widget["volume"].toggle()),
    Key([], "XF86AudioLowerVolume", lazy.widget["volume"].volume_down()),
    Key([], "XF86AudioRaiseVolume", lazy.widget["volume"].volume_up()),
    # Key([], "XF86MicMute", lazy.spawn("/home/sean/.qtile/volume.sh mic")),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

groups = [Group("%d" % (n+1)) for n in range(5)]

groups.append(
    Group('Xephyr', init=False, matches=[Match(wm_class=['Xephyr'])])
)

dgroups_key_binder = simple_key_binder(mod)
dgroups_app_rules = []

layouts = [
    layout.MonadTall(
        border_focus="#a0a0d0", border_normal="#202030", border_width=1
    ),
    layout.Max()
]

cyan = ["#00afff", "#8cfcff"]
red = ["#bb0000", "#990000"]
lt_grey = ["#828282", "#a4a4a4"]
med_grey = ["#494949", "#595959"]
grey = ["#656565", "#323232"]
dk_grey = ["#040404", "#292929"]

widget_defaults = dict(
    font="DejaVu",
    fontsize=11, padding=2, background=dk_grey
)

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

widgets1 = [
    widget.Prompt(prompt=prompt, padding=10,
                  background=grey),
    widget.TextBox(text="\u25e4 ", fontsize=42, padding=-8,
                   foreground=grey),
    widget.GroupBox(borderwidth=4, highlight_method='line', margin=0, disable_drag=True,
                    this_current_screen_border=cyan,
                    this_screen_border=lt_grey,
                    other_screen_border=med_grey,
                    urgent_border=red),
    widget.TextBox(text="\u25e4", fontsize=42, padding=-1,
                   foreground=dk_grey, background=grey),
    widget.TaskList(borderwidth=1, background=grey,
                    border=cyan, urgent_border=red),
    widget.TextBox(text="\u25e4 ", fontsize=42, padding=-8,
                   foreground=grey),
    #widget.TextBox(text=u'\U0001f321'),
    widget.Systray(),
    widget.TextBox(text="\u2328", foreground=cyan),
    widget.KeyboardLayout(configured_keyboards=["us dvorak", "us"], foreground=cyan, update_interval=5),
    tempsensor.TempSensor(font="fontawesome"),
    networkmonitor.NetworkMonitor(font="fontawesome"),
    volume.Volume(font="fontawesome"),
    widget.Clock(format='%m-%d-%Y %a %H:%M:%S'),
]

widgets2 = [
    widget.TextBox(text="\u25e4 ", fontsize=42, padding=-8,
                   foreground=grey),
    widget.GroupBox(borderwidth=4, highlight_method='line', margin=0, disable_drag=True,
                    this_current_screen_border=cyan,
                    this_screen_border=lt_grey,
                    other_screen_border=med_grey,
                    urgent_border=red),
    widget.TextBox(text="\u25e4", fontsize=42, padding=-1,
                   foreground=dk_grey, background=grey),
    widget.TaskList(borderwidth=1, background=grey,
                    border=cyan, urgent_border=red),
    widget.TextBox(text="\u25e4 ", fontsize=42, padding=-8,
                   foreground=grey),
    widget.TextBox(text="\u2328", foreground=cyan),
    widget.KeyboardLayout(configured_keyboards=["us dvorak", "us"], foreground=cyan, update_interval=5),
    tempsensor.TempSensor(font="fontawesome"),
    networkmonitor.NetworkMonitor(font="fontawesome"),
    volume.Volume(font="fontawesome"),
    widget.Clock(format='%m-%d-%Y %a %H:%M:%S'),
]

if os.path.exists('/sys/class/power_supply/BAT0'):
    widgets1.insert(-1, battery.Battery())

screens = [
    Screen(top=bar.Bar(widgets1, size=23)),
    Screen(top=bar.Bar(widgets2, size=23))
]

follow_mouse_focus = True
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
