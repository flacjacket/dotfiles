#!/bin/bash

filename=$1
title=$2

echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<!DOCTYPE Tags SYSTEM \"matroskatags.dtd\">

<Tags>
  <Tag>
    <Simple>
      <Name>Source</Name>
      <String>Video file</String>
    </Simple>
    <Simple>
      <Name>Title</Name>
      <String>${title}</String>
    </Simple>
    <Simple>
      <Name>Video Filters</Name>
      <String>crop=1440:1080:240:0</String>
    </Simple>
    <Simple>
      <Name>Audio Codec (Track 1)</Name>
      <String>DTS 5.1 @ 768Kbps</String>
    </Simple>
    <Simple>
      <Name>x264 parameters</Name>
      <String>--slow-firstpass --bitrate=12000 --me=umh --merange=24 --no-dct-decimate --8x8dct --no-fast-pskip --trellis=2 --partitions=p8x8,b8x8,i4x4,i8x8 --psy-rd=0.8,0.0 --ref=4 --bframes=5 --b-adapt=2 --weightp=1 --direct=auto --subme=9 --no-mbtree --rc-lookahead=100 --sync-lookahead=auto --cabac --aq-strength=0.8 --aq-mode=1 --deblock=-3,-3 --level=41</String>
    </Simple>
    <Simple>
      <Name>x264 version</Name>
      <String>0.110.x</String>
    </Simple>
    <Simple>
      <Name>mkvmerge version</Name>
      <String>4.4.0</String>
    </Simple>
  </Tag>
</Tags>" > "mkvtags.xml"

/usr/bin/mkvmerge  --global-tags "mkvtags.xml"  --title "${title}" --track-name 1:"Video"  --track-name 2:"DTS 5.1 @ 1536Kbps" "${filename}" -o "tmp.mkv" && mv -v "tmp.mkv" "${filename}"

rm mkvtags.xml
