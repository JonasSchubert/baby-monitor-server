#!/bin/sh

cvlc alsa://plughw:1,0 --sout '#transcode{vcodec=none,acodec=mp3,ab=128,channels=2,samplerate=44100}:std{access=http,mux=mp3,dst=:8081}'
