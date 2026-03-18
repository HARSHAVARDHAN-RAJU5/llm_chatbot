import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from config import CONFIG


def load_index():
    index = faiss.read_index(CONFIG["index_path"])
    with open(CONFIG["metadata_path"], "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata


def retrieve(query: str, model: SentenceTransformer, index, metadata) -> list[dict]:
    """
    Retrieve top-k relevant chunks for a query.
    Filters out chunks above similarity threshold.
    Returns list of dicts with text and score.
    """
    query_embedding = model.encode(query, convert_to_numpy=True).astype("float32")
    query_embedding = np.array([query_embedding])

    scores, indices = index.search(query_embedding, CONFIG["top_k"])

    results = []
    print(f"\n[Retrieval] Top-{CONFIG['top_k']} results for: '{query}'")
    print(f"[Retrieval] Similarity threshold (L2): {CONFIG['similarity_threshold']}")

    for idx, score in zip(indices[0], scores[0]):
        status = "✓ PASS" if score <= CONFIG["similarity_threshold"] else "✗ FILTERED"
        print(f"  Chunk {idx} | L2 Score: {score:.4f} | {status}")

        if score <= CONFIG["similarity_threshold"]:
            results.append({
                "chunk_id": idx,
                "text": metadata[idx]["text"],
                "score": float(score)
            })

    if not results:
        print("[Retrieval] No chunks passed threshold — returning top result anyway")
        idx, score = indices[0][0], scores[0][0]
        results.append({
            "chunk_id": int(idx),
            "text": metadata[idx]["text"],
            "score": float(score)
        })

    return results