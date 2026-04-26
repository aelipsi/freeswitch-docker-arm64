#BUILDKIT_PROGRESS=plain docker buildx build \
BUILDKIT_PROGRESS=plain screen -L docker buildx build \
  --platform linux/arm64 \
  --output type=docker,dest=whisper-server.tar \
  -t whisper-server:latest \
  .


