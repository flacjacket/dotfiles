#!/bin/sh

clean_exit () {
	[ -e index.html ] && rm index.html
	[ -e apod.jpg ] && rm apod.jpg
	[ -e candh-tmp.png ] && rm candh-tmp.png
	exit
}

cd ~/.apod/

wget http://apod.nasa.gov/apod/ -O index.html -q
if [ $? -ne 0 ]; then
	echo "$(date '+%d/%m/%y'): FAIL - Unable to fetch webpage"
	clean_exit
fi

img=`grep "<a href=\"image" index.html | cut -d\" -f 2`
if [ -z "$img" ]; then
	echo "$(date '+%d/%m/%y'): FAIL - Unable to find image"
	clean_exit
fi

wget "http://antwrp.gsfc.nasa.gov/apod/$img" -O apod.jpg -q
if [ $? -ne 0 ]; then
	echo "$(date '+%d/%m/%y'): FAIL - Unable to fetch image"
	clean_exit
fi

resolution=$(xdpyinfo | grep dimensions | perl -ne 'm/([0-9]{3,})x([0-9]{3,})/; print "$1x$2\n";' | head -n1 )
convert -resize $resolution apod.jpg apod.png

w=$(identify -format "%w" apod.png)
h=$(identify -format "%h" apod.png)
convert -gravity south -extent ${w}x${h} -background none candh.png candh-tmp.png

composite -gravity center candh-tmp.png apod.png apod.png

[ "$(w | grep xmonad)" ] && feh --bg-center apod.png

echo "$(date '+%d/%m/%y'): Success"

clean_exit
