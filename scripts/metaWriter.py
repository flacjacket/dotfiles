#!/usr/bin/python

import sys

indir = sys.argv[1]
outdir = sys.argv[2]
infile = outdir+"/"+sys.argv[3]
metamux = outdir+"/"+sys.argv[4]
metademux = outdir+"/"+sys.argv[5]
outfilebase = sys.argv[6]
mplsnum = sys.argv[7]

f = open(infile,'r')
s = f.read()
f.close()

pos = 0
tracks = []
files = []

for i in range(s.count("Track ID:")-s.count("Can't detect stream type")):
    pos = s.find("Track ID:    ",pos+1)
    pos1= s.find("\n",pos)
    trackid = s[pos+len("Track ID:    "):pos1]

    pos = s.find("Stream type: ",pos1)
    if pos != pos1+1:
        pos = pos1
        continue
    pos1= s.find("\n",pos)
    streamtype = s[pos+len("Stream type: "):pos1]
    if streamtype.find("VC-1")<0 and streamtype.find("DTS")<0:
        continue

    pos = s.find("Stream ID:   ",pos1)
    pos1= s.find("\n",pos)
    streamid = s[pos+len("Stream ID:   "):pos1]

    pos = s.find("Stream info: ",pos1)
    pos1= s.find("\n",pos)
    streaminfo = s[pos+len("Stream info: "):pos1]

    if streamtype == "VC-1":
        if streaminfo.find("1920:1080p")<0:
            continue
        pos2 = streaminfo.find("Frame rate: ")+len("Frame rate: ")
        pos3 = streaminfo.find(" ",pos2+1)
        framerate = streaminfo[pos2:pos3 if pos3>pos2 else len(streaminfo)]
        trackinfo="track="+trackid+", fps="+framerate
    else:
        trackinfo="track="+trackid
    tracks.append((streamid,trackinfo,streamtype))

pos = 0
for i in range(s.count("File #")):
    pos = s.find("File #",pos)
    pos1 = s.find("\n",pos)
    line = s[pos:pos1]
    files.append(line[line.rfind("/")+1:])
    pos = pos1

f = open(metamux,'w')
f.write("MUXOPT --no-pcr-on-video-pid --new-audio-pes --vbr --vbv-len=500\n")

for i in tracks:
    line=i[0]+", "
    for j in files:
        line+="\""+indir+"/"+j+"\"+"
    line=line[:len(line)-1]
    line += ", "+i[1]
    if i[2].find("DTS-HD")>=0:
        line += ", down-to-dts"
    line += ", mpls="+mplsnum+"\n"
    f.write(line)

f.close()

f = open(metademux,'w')
f.write("MUXOPT --no-pcr-on-video-pid --new-audio-pes --demux --vbr --vbv-len=500\n")

for i in tracks:
    line=i[0]+", \""+outdir+"/"+outfilebase+".ts\", "+i[1]+", mpls="+mplsnum+"\n"
    f.write(line)

f.close

f.close()
