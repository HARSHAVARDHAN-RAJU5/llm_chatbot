from sentence_transformers import SentenceTransformer
from config import CONFIG
from retrieval import load_index, retrieve
from generation import generate


def main():
    print("=" * 50)
    print("  RAG Knowledge Assistant (Local)")
    print(f"  Model : {CONFIG['embedding_model']}")
    print(f"  LLM   : {CONFIG['llm_model']}")
    print(f"  Top-K : {CONFIG['top_k']}")
    print("=" * 50)

    # Load once, reuse across queries
    print("[Setup] Loading embedding model...")
    model = SentenceTransformer(CONFIG["embedding_model"])
    index, metadata = load_index()
    print(f"[Setup] Index loaded | {index.ntotal} vectors\n")

    while True:
        query = input("Ask a question (or 'exit'): ").strip()
        if query.lower() in ("exit", "quit", "q"):
            break
        if not query:
            continue

        # Retrieve
        chunks = retrieve(query, model, index, metadata)

        # Generate
        answer = generate(query, chunks)

        print("\n--- ANSWER ---")
        print(answer)
        print("-" * 50 + "\n")


if __name__ == "__main__":
    main()