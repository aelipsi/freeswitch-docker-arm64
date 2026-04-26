#!/usr/bin/env python3

import numpy as np
import os
import asyncio
import websockets
import concurrent.futures
import logging
import json
import subprocess
import audioop


# =========================
# Config
# =========================

WHISPER_BIN = os.environ.get("WHISPER_CPP_BIN", "/opt/whisper/main")
MODEL_PATH = os.environ.get("WHISPER_MODEL_PATH", "/opt/whisper/models/ggml-tiny.bin")


# =========================
# Audio conversion
# =========================

def ulaw_to_pcm16(audio_bytes: bytes) -> np.ndarray:
    """
    Convert 8kHz μ-law → PCM16
    """
    pcm = audioop.ulaw2lin(audio_bytes, 2)
    return np.frombuffer(pcm, dtype=np.int16)


def resample_8k_to_16k(audio: np.ndarray) -> np.ndarray:
    """
    Simple linear interpolation resample (8k → 16k)
    """
    if len(audio) == 0:
        return audio

    return np.interp(
        np.linspace(0, len(audio), len(audio) * 2, endpoint=False),
        np.arange(len(audio)),
        audio
    ).astype(np.int16)


# =========================
# WebSocket chunk handling
# =========================

def process_chunk(message):
    if isinstance(message, str) and "uuid" in message:
        return None, False

    elif isinstance(message, str) and "grammar" in message:
        return message, False

    elif isinstance(message, str) and "eof" in message:
        return None, True

    else:
        # μ-law 8kHz → PCM16 → 16kHz PCM16
        pcm_8k = ulaw_to_pcm16(message)
        pcm_16k = resample_8k_to_16k(pcm_8k)
        return pcm_16k, False


# =========================
# whisper.cpp runner
# =========================

def run_whisper_cpp(audio: np.ndarray, prompt=""):
    """
    Run whisper.cpp via stdin (no files).
    """

    cmd = [
        WHISPER_BIN,
        "-m", MODEL_PATH,
        "-f", "-",
        "-nt",
        "-np"
    ]

    if prompt:
        cmd += ["--prompt", prompt]

    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = proc.communicate(audio.tobytes())

        if proc.returncode != 0:
            return f"ERROR: {stderr.decode('utf-8', errors='ignore')}"

        return stdout.decode("utf-8", errors="ignore").strip()

    except Exception as e:
        return f"ERROR: {e}"


# =========================
# WebSocket handler
# =========================

async def recognize(websocket):
    global pool

    audio_buffer = np.array([], dtype=np.int16)
    prompt_grammar = ""

    loop = asyncio.get_running_loop()

    logging.info("Connection from %s", websocket.remote_address)

    while True:
        message = await websocket.recv()

        response, stop = await loop.run_in_executor(
            pool,
            process_chunk,
            message
        )

        if isinstance(response, str):
            if "grammar" in response:
                try:
                    prompt_grammar = json.loads(response).get("grammar", "")
                except:
                    pass

        elif isinstance(response, np.ndarray):
            audio_buffer = np.concatenate((audio_buffer, response))

        if stop:
            if len(audio_buffer) == 0:
                continue

            text = await loop.run_in_executor(
                pool,
                run_whisper_cpp,
                audio_buffer,
                prompt_grammar
            )

            logging.info("Result: %s", text)
            await websocket.send(text)

            audio_buffer = np.array([], dtype=np.int16)


# =========================
# Server startup
# =========================

async def start():
    global pool

    logging.basicConfig(level=logging.INFO)

    interface = os.environ.get("WHISPER_SERVER_INTERFACE", "0.0.0.0")
    port = int(os.environ.get("WHISPER_SERVER_PORT", 2700))

    pool = concurrent.futures.ThreadPoolExecutor(
        os.cpu_count() or 1
    )

    async with websockets.serve(recognize, interface, port):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start())