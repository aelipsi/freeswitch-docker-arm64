# FreeSWTICH Docker container for Raspberry Pi
This is an inofficial Docker file for [FreeSWITCH](https://signalwire.com/freeswitch). It is based on [PatrickBaus's work](https://github.com/PatrickBaus/freeswitch-docker) but has build scripts and changes to do what I needed it to do. For more information, see the source README.

## Contents
- [H323 Support](#h323 support)
- [mod_whisper](#mod_whisper)

## H323 Support
There is a Dockerfile-H323 here that allows FreeSWITCH to build with mod_h323. I never ended up testing it, because I found SIP firmware for the phone I was testing with. However, building it was incredibly challenging so I wanted to share my work in the hopes that it might help some hobbiest.

## mod_whisper
I found a very interesting mod that is able to do ASR transcriptions powered by Whisper. I made some changes to the sample server to instead use whisper.cpp and also updated the build script to include mod_whisper in the build. 

