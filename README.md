# FreeSWTICH Docker container for Raspberry Pi
These are unofficial Docker builds for [FreeSWITCH](https://signalwire.com/freeswitch). It is based on [PatrickBaus's work](https://github.com/PatrickBaus/freeswitch-docker) but has build scripts and changes to do what I needed it to do. Note that the Docker builds are hard-coded for arm64 as I only care about running the containers on my Rasperry Pi. I probably won't be updating this repository after the initial release. It's for a hobby project, but seeing how popular FreeSWITCH is, I figured I could contribute to the open source community.

For more information, see the source README.

## Contents
- [H323 Support](#h323 support)
- [mod_whisper](#mod_whisper)

## H323 Support
There is a Dockerfile-H323 here that allows FreeSWITCH to build with mod_h323. Although it does compile, I never ended up testing it at runtime because I found SIP firmware for the phone I was testing with. However, building it was incredibly challenging due to only a vague note in the mod source and a lot of dependencies to compile so I wanted to share my work in the hopes that it might help some hobbiest in the future. I can confirm that it does NOT work, due to a linkage issue that I'm not going to try to fix.

## mod_whisper
I found a very interesting mod that is able to do automatic speech recognition powered by Whisper. I made some changes to the sample server to instead use whisper.cpp and also updated the build script to include mod_whisper in the build. 

Side note - has anybody ever done an ASR stream on Twitch? I imagine it'd be like an ASMR stream, but instead somebody just says words and checks to see if an automated system recognizes it.