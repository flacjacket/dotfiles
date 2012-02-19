#!/bin/sh

clean () {
	[ -e index.html ] && rm index.html
	[ -e apod.jpg ] && rm apod.jpg
	[ -e candh-tmp1.png ] && rm candh-tmp1.png
	[ -e candh-tmp2.png ] && rm candh-tmp2.png
}

log () {
	echo "$(date '+%d/%m/%y'): $1"
}

cd ~/.apod/

wget http://apod.nasa.gov/apod/ -O index.html -q
if [ $? -ne 0 ]; then
	log "FAIL - Unable to fetch webpage"
	clean
	exit
fi

img=`grep "<a href=\"image" index.html | cut -d\" -f 2`
if [ -z "$img" ]; then
	log "FAIL - Unable to find image"
	clean
	exit
fi

wget "http://antwrp.gsfc.nasa.gov/apod/$img" -O apod.jpg -q
if [ $? -ne 0 ]; then
	log "FAIL - Unable to fetch image"
	clean
	exit
fi

if $(xdpyinfo > /dev/null 2>&1); then
	WIDTH=$(xdpyinfo | grep dimensions | perl -ne 'm/([0-9]{3,})x([0-9]{3,})/; print "$1";' | head -n1 )
	HEIGHT=$(xdpyinfo | grep dimensions | perl -ne 'm/([0-9]{3,})x([0-9]{3,})/; print "$2";' | head -n1 )
else
	if [ -e default_size.sh ]; then
		source ./default_size.sh
	else
		log "FAIL - Cannot find screen size"
		clean
		exit
	fi
fi

convert -resize "${WIDTH}x${HEIGHT}" apod.jpg apod.png
convert -resize "${WIDTH}x${HEIGHT}" candh.png candh-tmp1.png

convert -extent "${WIDTH}x${HEIGHT}" -background none -gravity South candh-tmp1.png candh-tmp2.png

composite -gravity South candh-tmp2.png apod.png apod.png

[ "$(w | grep xmonad)" ] && feh --bg-center apod.png

log "Success"
clean
