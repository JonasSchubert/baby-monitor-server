#!/bin/sh

# https://github.com/srinathava/raspberry-pi-sleep-monitor/blob/master/gstream_video.sh

# The following gstreamer pipeline(s) 
# 1. broadcast OPUS encoded audio to UDP port 5002 which is then converted
#    to a WebRTC stream by Janus 
# 2. broadcast raw JPEG frames to TCP port 9999. This is then read in by
#    the mpeg_server.py script and packaged into a multi-part stream so
#    that a browser can display it
# 
# A few subtle points in this pipeline which took some debugging to figure
# out:
# 1. tcpclient needs to have the host property set otherwise it tries to
# use a IPV6 instead of IPV4 port.
# 2. Need to use queue's after the tee branches otherwise the second branch
# of the tee "stalls" i.e., never seems to run.

sleep 3 # wait for reactor to be started

videosrc=/dev/video0
if [ $1 != "" ]; then
    videosrc=$1
fi

export GST_V4L2_USE_LIBV4L2=1 # https://gstreamer.freedesktop.org/documentation/video4linux2/v4l2src.html?gi-language=c

gst-launch-1.0 -v \
    libcamerasrc \
        ! video/x-raw,framerate=10/1, width=640, height=480 \
        ! clockoverlay valignment=bottom time-format="%H:%M" \
        ! jpegenc \
        ! videorate \
        ! multipartmux boundary=spionisto \
        ! tcpclientsink host=127.0.0.1 port=9999
