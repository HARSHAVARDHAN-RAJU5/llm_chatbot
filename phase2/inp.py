import faiss
import json
import numpy as np
import subprocess
from sentence_transformers import SentenceTransformer

# Load FAISS index
index = faiss.read_index("../phase1/vector_index.faiss")

# Load metadata
with open("../phase1/vector_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Ask question
qn = input("ask question: ")

# Encode query
qn_embedding = model.encode(qn)
qn_embedding = np.array([qn_embedding]).astype("float32")

# Retrieve
k = 1
scores, indices = index.search(qn_embedding, k)

# Collect context
context = ""
for idx, score in zip(indices[0], scores[0]):
    context += metadata[idx]["text"] + "\n\n"

# Build internal prompt
prompt = f"""
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{qn}

Answer:
"""

# Call local LLM (Ollama)
result = subprocess.run(
    ["ollama", "run", "llama3"],
    input=prompt,
    text=True,
    capture_output=True
)

print("\n--- ANSWER ---")
print(result.stdout)
