#!/bin/bash

ep=$1
mpls=$2
dir=`pwd`
out="${dir}/${ep}"
tmp="${dir}/${ep}/tmp"
pyscript="${HOME}/metaWriter.py"

mplsFile="../PLAYLIST/${mpls}.mpls"
tsmuxOutput="tsmux.out"
tsmuxMeta1="tsmux-mux.meta"
tsmuxMeta2="tsmux-demux.meta"
tsmuxFileBase="input"
fifoFile="${tmp}/fifo.yuv"
x264Log="${tmp}/x264.log"
tmpVideo="${tmp}/video.h264"

outVideo="${out}/output-${mpls}.mkv"

x264opts="--slow-firstpass --bitrate=12000 --me=umh --merange=24 --no-dct-decimate --8x8dct --no-fast-pskip --trellis=2 --partitions=p8x8,b8x8,i4x4,i8x8 --psy-rd=0.8,0.0 --ref=4 --bframes=5 --b-adapt=2 --weightp=1 --direct=auto --subme=9 --no-mbtree --rc-lookahead=100 --sync-lookahead=auto --cabac --aq-strength=0.8 --aq-mode=1 --deblock=-3,-3 --level=41"
x264pass1opts="--pass=1"
x264pass2opts="--pass=2"

test -e "${mplsFile}" || { echo "Playlist file missing"; exit 1; }
test -e "${pyscript}" || { echo "Python script not found"; exit 1; }

test -d "${out}" || mkdir -p "${out}"
test -d "${tmp}" || mkdir -p "${tmp}"
test -e "${outVideo}" && mv -f "${outVideo}" "${outVideo}.old"

nice -n 10 tsMuxeR "../PLAYLIST/${mpls}.mpls" > "${tmp}/${tsmuxOutput}"
python "${pyscript}" "${dir}" "${tmp}" "${tsmuxOutput}" "${tsmuxMeta1}" "${tsmuxMeta2}" "${tsmuxFileBase}" "${mpls}"
nice -n 10 tsMuxeR "${tmp}/${tsmuxMeta1}" "${tmp}/${tsmuxFileBase}.ts"
nice -n 10 tsMuxeR "${tmp}/${tsmuxMeta2}" "${tmp}"

dtsfile=`ls "${tmp}/${tsmuxFileBase}.track_"*.dts`
vc1file=`ls "${tmp}/${tsmuxFileBase}.track_"*.vc1`

test -e "${fifoFile}" && rm "${fifoFile}"
mkfifo "${fifoFile}"

nice -n 10 ffmpeg -i "${vc1file}" -f yuv4mpegpipe -vf "crop=1440:1080:240:0" - 2> /dev/null > "${fifoFile}" & \
nice -n 10 x264 "${fifoFile}" ${x264pass1opts} --stats="${x264Log}" ${x264opts} -o "/dev/null" --demuxer y4m

rm "${fifoFile}"
mkfifo "${fifoFile}"

nice -n 10 ffmpeg -i "${vc1file}" -f yuv4mpegpipe -vf "crop=1440:1080:240:0" - 2> /dev/null > "${fifoFile}" & \
nice -n 10 x264 "${fifoFile}" ${x264pass2opts} --stats="${x264Log}" ${x264opts} -o "${tmpVideo}" --demuxer y4m

rm "${fifoFile}"

nice -n 10 mkvmerge --title "${ep}" --track-name 0:"Video" --default-duration 0:23.976fps "${tmpVideo}" --track-name 0:"DTS 5.1 @ 1536Kbps" "${dtsfile}" -o "${outVideo}"

rm -r "${tmp}"
