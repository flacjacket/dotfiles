#!/bin/sh

run ()
{
	wget http://apod.nasa.gov/apod/ -O index.html -q
	if [ $? -ne 0 ]; then
		echo "$(date '+%d/%m/%y'): FAIL - Unable to fetch webpage"
		exit
	fi

	img=`grep "<a href=\"image" index.html | cut -d\" -f 2`
	if [ -z "$img" ]; then
		echo "$(date '+%d/%m/%y'): FAIL - Unable to find image"
		exit
	fi

	wget "http://antwrp.gsfc.nasa.gov/apod/$img" -O apod.jpg -q
	if [ $? -ne 0 ]; then
		echo "$(date '+%d/%m/%y'): FAIL - Unable to fetch image"
		exit
	fi

	convert -resize 1920x1200 apod.jpg apod.png
	if [ $? -ne 0 ]; then
		echo "$(date '+%d/%m/%y'): FAIL - Unable to convert image"
		exit
	fi

	feh --bg-center apod.png
	if [ $? -ne 0 ]; then
		echo "$(date '+%d/%m/%y'): FAIL - Unable to set image"
	else
		echo "$(date '+%d/%m/%y'): Success"
	fi
}

pwd=`pwd`
cd ~/.apod/
run
[ -e index.html ] && rm index.html
[ -e apod.jpg ] && rm apod.jpg
cd "$pwd"
