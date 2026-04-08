import ollama
import requests
import pygame
from config import CONFIG


def build_prompt(query: str, context_chunks: list[dict]) -> str:
    context = "\n\n".join([c["text"] for c in context_chunks])
    return f"""Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know based on the provided context."

Context:
{context}

Question:
{query}

Answer:"""


def generate(query: str, context_chunks: list[dict]) -> str:
    prompt = build_prompt(query, context_chunks)

    print(f"[Generation] Calling {CONFIG['llm_model']} via Ollama...")
    response = ollama.chat(
        model=CONFIG["llm_model"],
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response["message"]["content"]

    speak(answer)
    return answer


def speak(text: str):
    print("[TTS] Sending to ElevenLabs...")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{CONFIG['elevenlabs_voice_id']}"
    headers = {
        "xi-api-key": CONFIG["elevenlabs_api_key"],
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": CONFIG["elevenlabs_tts_model"],
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        audio_file = "output_audio.mp3"
        with open(audio_file, "wb") as f:
            f.write(response.content)
        print("[TTS] Playing audio...")
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
    else:
        print(f"[TTS] Error: {response.status_code} — {response.text}")