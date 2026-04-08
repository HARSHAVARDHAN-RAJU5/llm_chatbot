# Voice RAG Assistant

A local Retrieval-Augmented Generation (RAG) pipeline with a full voice loop — speak a question, get a spoken answer.

## Pipeline

```
Voice Input (mic)
     ↓
[STT]        — ElevenLabs Scribe (speech-to-text)
     ↓
[Retrieval]  — FAISS vector search over embedded document chunks
     ↓
[Generation] — Ollama (Llama3) with injected context
     ↓
[TTS]        — ElevenLabs (text-to-speech, custom voice)
     ↓
Spoken Answer
```

Also supports plain text input mode.

## Stack

| Component | Tool |
|---|---|
| STT | ElevenLabs Scribe |
| Embeddings | `sentence-transformers` (all-MiniLM-L6-v2) |
| Vector Search | FAISS (L2 similarity) |
| LLM | Ollama (Llama3) |
| TTS | ElevenLabs |
| Language | Python 3.10+ |

## Setup

```bash
pip install faiss-cpu sentence-transformers ollama numpy requests sounddevice soundfile
ollama pull llama3
sudo apt install mpg123   # for audio playback on Linux
```

Add your ElevenLabs API key to `config.py`:
```python
"elevenlabs_api_key": "YOUR_API_KEY_HERE"
```

## Usage

**Step 1 — Build index from your document:**
```bash
python indexing.py
```

**Step 2 — Run the voice assistant:**
```bash
python main.py
```

Choose `v` for voice input or `t` for text input when prompted.

## Configuration

Edit `config.py`:

| Parameter | Default | Effect |
|---|---|---|
| `chunk_size` | 500 | Larger = more context per chunk |
| `overlap_paragraphs` | 1 | Higher = better continuity |
| `top_k` | 3 | More chunks = richer context |
| `similarity_threshold` | 1.2 | Lower = stricter relevance filter |
| `elevenlabs_voice_id` | — | Voice used for TTS output |
| `elevenlabs_tts_model` | eleven_turbo_v2 | Speed/quality tradeoff |

## Project Structure

```
├── config.py       # All tunable parameters
├── ingestion.py    # Chunking with overlap
├── indexing.py     # Embedding + FAISS indexing
├── retrieval.py    # Query → vector search → threshold filter
├── generation.py   # Prompt construction + Ollama + TTS
├── main.py         # Voice/text input loop + STT
├── data/           # Place source documents here
└── store/          # Generated index and metadata
```