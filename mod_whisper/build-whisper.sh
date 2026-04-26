#!/bin/bash

BUILDKIT_PROGRESS=plain screen -L docker buildx build -f Dockerfile-whisper \
  --platform linux/arm64 \
  --output type=docker,dest=freeswitch-whisper.tar \
  -t freeswitch-whisper:latest \
  ..
