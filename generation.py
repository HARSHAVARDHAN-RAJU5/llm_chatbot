import ollama
from config import CONFIG


def build_prompt(query: str, context_chunks: list[dict]) -> str:
    context = "\n\n".join([c["text"] for c in context_chunks])
    return f"""Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know based on the provided context."

Context:
{context}

Question:
{query}

Answer:"""


def generate(query: str, context_chunks: list[dict]) -> str:
    prompt = build_prompt(query, context_chunks)

    print(f"[Generation] Calling {CONFIG['llm_model']} via Ollama...")
    response = ollama.chat(
        model=CONFIG["llm_model"],
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]