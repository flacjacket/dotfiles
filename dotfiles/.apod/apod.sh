#!/bin/sh

clean () {
	[ -e index.html ] && rm index.html
	[ -e apod.jpg ] && rm apod.jpg
	[ -e candh-tmp1.png ] && rm candh-tmp1.png
	[ -e candh-tmp2.png ] && rm candh-tmp2.png
}

cd ~/.apod/

wget http://apod.nasa.gov/apod/ -O index.html -q
if [ $? -ne 0 ]; then
	echo "$(date '+%d/%m/%y'): FAIL - Unable to fetch webpage"
	clean
	exit
fi

img=`grep "<a href=\"image" index.html | cut -d\" -f 2`
if [ -z "$img" ]; then
	echo "$(date '+%d/%m/%y'): FAIL - Unable to find image"
	clean
	exit
fi

wget "http://antwrp.gsfc.nasa.gov/apod/$img" -O apod.jpg -q
if [ $? -ne 0 ]; then
	echo "$(date '+%d/%m/%y'): FAIL - Unable to fetch image"
	clean
	exit
fi

resolution=$(xdpyinfo | grep dimensions | perl -ne 'm/([0-9]{3,})x([0-9]{3,})/; print "$1x$2\n";' | head -n1 )
convert -resize $resolution apod.jpg apod.png
convert -resize $resolution candh.png candh-tmp1.png

w=$(identify -format "%w" apod.png)
h=$(identify -format "%h" apod.png)
convert -gravity south -extent ${w}x${h} -background none candh-tmp1.png candh-tmp2.png

composite -gravity center candh-tmp2.png apod.png apod.png

[ "$(w | grep xmonad)" ] && feh --bg-center apod.png

echo "$(date '+%d/%m/%y'): Success"

clean
