import faiss
import json
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from config import CONFIG
from ingestion import ingest


def build_index(source_path: str):
    # Step 1: Ingest
    chunks = ingest(source_path)
    texts = [c["text"] for c in chunks]

    # Step 2: Embed
    print(f"[Embedding] Loading model: {CONFIG['embedding_model']}")
    model = SentenceTransformer(CONFIG["embedding_model"])
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True).astype("float32")
    print(f"[Embedding] Shape: {embeddings.shape}")

    # Step 3: Index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    print(f"[Indexing] Vectors stored: {index.ntotal}")

    # Step 4: Save
    os.makedirs("store", exist_ok=True)
    faiss.write_index(index, CONFIG["index_path"])
    with open(CONFIG["metadata_path"], "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(f"[Indexing] Saved index → {CONFIG['index_path']}")
    print(f"[Indexing] Saved metadata → {CONFIG['metadata_path']}")


if __name__ == "__main__":
    build_index("data/clean_text.txt")