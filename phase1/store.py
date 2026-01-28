import faiss
import numpy as np
import json

embeddings = np.load("embeddings.npy").astype("float32")

with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)

index.add(embeddings)

faiss.write_index(index, "vector_index.faiss")

with open("vector_metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print("Stored successfully")
print("Vectors:", index.ntotal)
print("Dimension:", dim)