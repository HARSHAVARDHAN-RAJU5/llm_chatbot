from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("chunks.txt", "r", encoding="utf-8") as f:
    raw = f.read()

chunks = [
    chunk.strip()
    for chunk in raw.split("--- Chunk")
    if chunk.strip()
]

embeddings = model.encode(
    chunks,
    show_progress_bar=True,
    convert_to_numpy=True
)

np.save("embeddings.npy", embeddings)

with open("chunks_save.txt", "w", encoding="utf-8") as f:
    for chunk in chunks:
        f.write(chunk + "\n---\n")

print("Embeddings created:")
print("• Total chunks:", len(chunks))
print("• Embedding shape:", embeddings.shape)
