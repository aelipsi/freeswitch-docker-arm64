# FreeSWTICH Docker container for Raspberry Pi
These are unofficial Docker builds for [FreeSWITCH](https://signalwire.com/freeswitch). It is based on [PatrickBaus's work](https://github.com/PatrickBaus/freeswitch-docker) but has build scripts and changes to do what I needed it to do. Note that the Docker builds are hard-coded for arm64 as I only care about running the containers on my Rasperry Pi. I probably won't be updating this repository after the initial release. It's for a hobby project, but seeing how popular FreeSWITCH is, I figured I could contribute to the open source community.

For more information, see the upstream project README.

## Contents
- [H323 Support](#h323 support)
- [mod_whisper](#mod_whisper)

## H323 Support
There is a Dockerfile-H323 here that allows FreeSWITCH to build with mod_h323. Although it does compile, I never ended up testing it at runtime because I found SIP firmware for the phone I was testing with. However, building it was incredibly challenging due to only a vague note in the mod source and a lot of dependencies to compile so I wanted to share my work in the hopes that it might help some hobbiest in the future. I can confirm that FreeSWITCH loads the module properly with the following logs. Anything further [I don't have time to try to fix](https://github.com/freeswitch/freeswitch-sounds/raw/refs/heads/master/en/us/callie/ivr/48000/ivr-file_a_jira.wav). 

```
2026-04-26 19:48:38.922714 0.00% [DEBUG] mod_h323.cpp:372 ======>FSProcess::Initialise [0x7fa3cc2ab0]
2026-04-26 19:48:38.923425 0.00% [DEBUG] mod_h323.cpp:608 ======>FSH323EndPoint::FSH323EndPoint [0x7fa39d7f60]
2026-04-26 19:48:38.923534 0.00% [DEBUG] mod_h323.cpp:380 ======>FSManager::Initialise [0x7fa39d7f60]
2026-04-26 19:48:38.923551 0.00% [DEBUG] mod_h323.cpp:462 ======>FSH323EndPoint::ReadConfig [0x7fa39d7f60]
2026-04-26 19:48:38.923676 0.00% [ERR] mod_h323.cpp:485 open of h323.conf failed            <----- be sure to update autoload_configs to have the h323 config file
2026-04-26 19:48:38.923713 0.00% [DEBUG] mod_h323.cpp:394 Config capability
2026-04-26 19:48:38.923731 0.00% [DEBUG] mod_h323.cpp:428 --->fax_asn
2026-04-26 19:48:38.924596 0.00% [NOTICE] switch_loadable_module.c:172 Adding Endpoint 'h323'
```

## mod_whisper
I found a very interesting mod that is able to do automatic speech recognition powered by Whisper. I made some changes to the sample server to instead use whisper.cpp and also updated the build script to include mod_whisper in the build. Haven't actually tested it yet, so I may push updates to that in the future.

Side note - has anybody ever done an ASR stream on Twitch? I imagine it'd be like an ASMR stream, but instead somebody just says words and checks to see if an automated system recognizes it. Guess it'd have a very niche audience.
