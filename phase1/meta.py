import json
import numpy as np

embeddings = np.load("embeddings.npy")

with open("chunks.txt", "r", encoding="utf-8") as f:
    raw = f.read()

chunks = [
    c.strip()
    for c in raw.split("--- Chunk")
    if c.strip()
]

assert len(chunks) == embeddings.shape[0], "Chunks and embeddings count mismatch"

metadata = []

for i, chunk in enumerate(chunks):
    metadata.append({
        "chunk_id": i,
        "text": chunk,
        "source": "python_pdf",
        "section": chunk.split("\n")[0]
    })

with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print("Metadata saved")
print("Total chunks:", len(metadata))
