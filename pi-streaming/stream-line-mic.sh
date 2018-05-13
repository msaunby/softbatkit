#!/bin/sh

Record_from_Linein_Micbias.sh
#arecord -f S16_LE -c2 -r192000 | ffmpeg -i -  -b:a 512k -bufsize 2M -ar 192000 -f mulaw -f rtp rtp://192.168.0.22:1234
arecord -f S16_LE -c2 -r192000 | ffmpeg -i -  -b:a 512k -bufsize 2M -ar 192000 -f s16le -f rtp rtp://192.168.0.22:1234

#mulaw SDP:
#v=0
#o=- 0 0 IN IP4 127.0.0.1
#s=No Name
#c=IN IP4 192.168.0.22
#t=0 0
#a=tool:libavformat 57.56.101
#m=audio 1234 RTP/AVP 97
#b=AS:128
#a=rtpmap:97 PCMU/192000/2
#
#s16le SDP:
#v=0
#o=- 0 0 IN IP4 127.0.0.1
#s=No Name
#c=IN IP4 192.168.0.22
#t=0 0
#a=tool:libavformat 57.71.100
#m=audio 1234 RTP/AVP 97
#b=AS:3072
#a=rtpmap:97 PCMU/192000/2

# SDL_AUDIODRIVER="alsa" AUDIODEV="hw:Loopback,1,0" ffplay  -vn -nodisp -b:a 512k -bufsize 2M -i stream.spd
