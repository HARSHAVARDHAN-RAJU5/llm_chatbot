CONFIG = {
    "chunk_size": 500,
    "overlap_paragraphs": 1,
    "top_k": 3,
    "similarity_threshold": 1.2,
    "embedding_model": "all-MiniLM-L6-v2",
    "llm_model": "llama3",
    "index_path": "store/vector_index.faiss",
    "metadata_path": "store/vector_metadata.json",

    # ElevenLabs
    "elevenlabs_api_key": "YOUR_API_KEY_HERE",
    "elevenlabs_voice_id": "flHkNRp1BlvT73UL6gyz",
    "elevenlabs_stt_model": "scribe_v1",
    "elevenlabs_tts_model": "eleven_turbo_v2",
}