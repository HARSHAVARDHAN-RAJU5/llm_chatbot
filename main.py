import requests
import keyboard
import sounddevice as sd
import soundfile as sf
import numpy as np
import pygame
import os
from sentence_transformers import SentenceTransformer
from config import CONFIG
from retrieval import load_index, retrieve
from generation import generate


SAMPLE_RATE = 16000


def record_until_release(filename="input_audio.wav"):
    print("[STT] Hold SPACE to record, release to stop...")
    keyboard.wait("space")
    print("[STT] Recording...")

    frames = []

    def callback(indata, frame_count, time_info, status):
        frames.append(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1,
                        dtype="int16", callback=callback):
        keyboard.wait("space", suppress=False, trigger_on_release=True)

    print("[STT] Stopped recording")
    audio = np.concatenate(frames, axis=0)
    sf.write(filename, audio, SAMPLE_RATE)
    return filename


def transcribe(filename: str) -> str:
    print("[STT] Transcribing via ElevenLabs...")
    url = "https://api.elevenlabs.io/v1/speech-to-text"
    headers = {"xi-api-key": CONFIG["elevenlabs_api_key"]}
    with open(filename, "rb") as f:
        files = {"file": (filename, f, "audio/wav")}
        data = {"model_id": CONFIG["elevenlabs_stt_model"]}
        response = requests.post(url, headers=headers, files=files, data=data)

    if response.status_code == 200:
        text = response.json().get("text", "")
        print(f"[STT] Transcribed: {text}")
        return text
    else:
        print(f"[STT] Error: {response.status_code} — {response.text}")
        return ""


def main():
    print("=" * 50)
    print("  Voice RAG Assistant")
    print(f"  Embedding : {CONFIG['embedding_model']}")
    print(f"  LLM       : {CONFIG['llm_model']}")
    print(f"  Voice ID  : {CONFIG['elevenlabs_voice_id']}")
    print("=" * 50)
    print("  Type your question and press Enter")
    print("  OR hold SPACE to speak, release to send")
    print("  Type 'exit' to quit")
    print("=" * 50 + "\n")

    print("[Setup] Loading embedding model...")
    model = SentenceTransformer(CONFIG["embedding_model"])
    index, metadata = load_index()
    print(f"[Setup] Index loaded | {index.ntotal} vectors\n")

    while True:
        if keyboard.is_pressed("space"):
            audio_file = record_until_release()
            query = transcribe(audio_file)
        else:
            query = input("Your question (or hold SPACE to speak): ").strip()

        if not query or query.lower() in ("exit", "quit", "q"):
            break

        chunks = retrieve(query, model, index, metadata)
        answer = generate(query, chunks)

        print("\n--- ANSWER ---")
        print(answer)
        print("-" * 50 + "\n")


if __name__ == "__main__":
    main()