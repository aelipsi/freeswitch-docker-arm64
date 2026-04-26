#!/bin/bash
#
BUILDKIT_PROGRESS=plain screen -L docker buildx build -f Dockerfile-h323 \
  --platform linux/arm64 \
  --output type=docker,dest=freeswitch-h323.tar \
  -t freeswitch-h323:latest \
  ..
