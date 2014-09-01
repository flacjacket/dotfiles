#!/bin/sh

if [ "x$1" == "xmute" ]; then
    amixer -q sset Master toggle
elif [ "x$1" == "xup" ]; then
    amixer -q sset Master 4+
elif [ "x$1" == "xdown" ]; then
    amixer -q sset Master 4-
fi

PERCENT=`amixer sget Master | sed -ne 's/^ *Mono: .*\[\([0-9]*\)%\].*$/\1/p'`
MUTE=`amixer sget Master | sed -ne 's/^ *Mono: .*\[\([onf]\{2,3\}\)\]$/\1/p'`
BAR=`echo $PERCENT | gdbar`

if [ "$MUTE" == "off" ]; then
    ICON="/home/sean/.dzen/icons/volume-mute.xbm"
elif [ $PERCENT -gt 75 ]; then
    ICON="/home/sean/.dzen/icons/volume-100.xbm"
elif [ $PERCENT -gt 50 ]; then
    ICON="/home/sean/.dzen/icons/volume-75.xbm"
elif [ $PERCENT -gt 25 ]; then
    ICON="/home/sean/.dzen/icons/volume-50.xbm"
else
    ICON="/home/sean/.dzen/icons/volume-25.xbm"
fi

PERCENT=`printf "%3d" $PERCENT`
n=`xrandr | grep ' connected' | cut -f1 -d' ' | wc -l`
for i in `seq 1 $n`; do
    echo "^fg(white) ^i($ICON) $BAR $PERCENT%" | dzen2 -p 4 -ta c -x -190 -w 170 -y 20 -fn -*-terminus-*-r-normal-*-*-90-*-*-*-*-iso8859-* -xs $i &
done
