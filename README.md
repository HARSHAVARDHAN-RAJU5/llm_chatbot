# RAG Knowledge Assistant

A fully local Retrieval-Augmented Generation (RAG) pipeline for domain-specific Q&A.

## Pipeline

```
Document (PDF/Text)
     ↓
[Ingestion]  — overlap-based chunking (configurable chunk_size, overlap)
     ↓
[Embedding]  — Sentence Transformers (all-MiniLM-L6-v2)
     ↓
[Indexing]   — FAISS (IndexFlatL2, vector similarity search)
     ↓
[Retrieval]  — top-k chunks filtered by similarity threshold
     ↓
[Generation] — Ollama (Llama3/Mistral) with injected context prompt
     ↓
Answer
```

## Stack

| Component | Tool |
|---|---|
| Embeddings | `sentence-transformers` (all-MiniLM-L6-v2) |
| Vector Search | `FAISS` (L2 similarity) |
| LLM | `Ollama` (Llama3 / Mistral) |
| Language | Python 3.10+ |

## Setup

```bash
pip install faiss-cpu sentence-transformers ollama numpy
ollama pull llama3
```

## Usage

**Step 1 — Build index from your document:**
```bash
# Place your text file at data/clean_text.txt
python indexing.py
```

**Step 2 — Query:**
```bash
python main.py
```

## Configuration

Edit `config.py` to tune:

| Parameter | Default | Effect |
|---|---|---|
| `chunk_size` | 500 | Larger = more context per chunk |
| `overlap_paragraphs` | 1 | Higher = better continuity |
| `top_k` | 3 | More chunks = richer context |
| `similarity_threshold` | 1.2 | Lower = stricter relevance filter |

## Project Structure

```
├── config.py       # All tunable parameters
├── ingestion.py    # Chunking with overlap
├── indexing.py     # Embedding + FAISS indexing
├── retrieval.py    # Query → vector search → threshold filter
├── generation.py   # Prompt construction + Ollama call
├── main.py         # Entry point
├── data/           # Place source documents here
└── store/          # Generated index and metadata
```