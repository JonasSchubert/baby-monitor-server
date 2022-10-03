#!/bin/sh

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
