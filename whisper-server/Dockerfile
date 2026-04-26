FROM python:3.14-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir websockets 

# Build whisper.cpp
RUN git clone --depth 1 --branch v1.8.4 https://github.com/ggerganov/whisper.cpp.git /opt/whisper
WORKDIR /opt/whisper
RUN make -j$(nproc)

# Download a small model (tiny)
RUN apt-get update && apt-get install -y \
    curl  \
    && rm -rf /var/lib/apt/lists/*

RUN ./models/download-ggml-model.sh tiny
WORKDIR /app

RUN pip install --no-cache-dir numpy

COPY server.py .

RUN apt purge -y \
    build-essential \
    cmake \
    git \
    ffmpeg

RUN pip install --no-cache-dir audioop-lts

USER appuser

CMD ["python", "server.py"]
