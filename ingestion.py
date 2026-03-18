import json
import os
from config import CONFIG


def chunk_document(text: str) -> list[dict]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    max_chars = CONFIG["chunk_size"]
    overlap = CONFIG["overlap_paragraphs"]

    chunks = []
    current_chunk = []
    current_length = 0

    for para in paragraphs:
        para_length = len(para)

        if current_length + para_length <= max_chars:
            current_chunk.append(para)
            current_length += para_length
        else:
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
            # Overlap: carry last N paragraphs into next chunk
            carry = current_chunk[-overlap:] if overlap else []
            current_chunk = carry + [para]
            current_length = sum(len(p) for p in current_chunk)

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return [{"chunk_id": i, "text": chunk} for i, chunk in enumerate(chunks)]


def ingest(source_path: str) -> list[dict]:
    """
    Load a text file and return chunked metadata.
    """
    with open(source_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_document(text)
    print(f"[Ingestion] {len(chunks)} chunks created from '{source_path}'")
    print(f"[Ingestion] Config: chunk_size={CONFIG['chunk_size']}, overlap={CONFIG['overlap_paragraphs']}")
    return chunks


if __name__ == "__main__":
    chunks = ingest("data/clean_text.txt")
    os.makedirs("store", exist_ok=True)
    with open("store/chunks_preview.txt", "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(f"--- Chunk {c['chunk_id']} ---\n{c['text']}\n\n")
    print("[Ingestion] Preview saved to store/chunks_preview.txt")