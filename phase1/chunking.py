with open("clean_text.txt", "r", encoding="utf-8") as f:
    clean_text = f.read()

paragraphs = [p.strip() for p in clean_text.split("\n\n") if p.strip()]

MAX_CHARS = 500
OVERLAP_PARAGRAPHS = 1  

chunks = []
current_chunk = []
current_length = 0

for para in paragraphs:
    para_length = len(para)

    if current_length + para_length <= MAX_CHARS:
        current_chunk.append(para)
        current_length += para_length
    else:
        chunks.append("\n\n".join(current_chunk))
        overlap = current_chunk[-OVERLAP_PARAGRAPHS:] if OVERLAP_PARAGRAPHS else []
        current_chunk = overlap + [para]
        current_length = sum(len(p) for p in current_chunk)

if current_chunk:
    chunks.append("\n\n".join(current_chunk))

# Save chunks to file
with open("chunks.txt", "w", encoding="utf-8") as f:
    for i, chunk in enumerate(chunks):
        f.write(f"--- Chunk {i+1} ---\n")
        f.write(chunk + "\n\n")

# import spacy

# nlp = spacy.load("en_core_web_sm")

# with open("clean_text.txt", "r", encoding="utf-8") as f:
#     text = f.read()

# lines = [line.strip() for line in text.split("\n") if line.strip()]

# MAX_CHARS = 700   

# chunks = []
# current_chunk = ""
# current_heading = None

# def is_heading(line):
#     return (
#         len(line) < 60 and
#         line.isalpha() or
#         line.istitle()
#     )

# for line in lines:
#     if is_heading(line):
#         if current_chunk:
#             chunks.append(current_chunk.strip())
#         current_heading = line
#         current_chunk = line + "\n\n"
#         continue

#     doc = nlp(line)
#     for sent in doc.sents:
#         sent_text = sent.text.strip()
#         if len(current_chunk) + len(sent_text) <= MAX_CHARS:
#             current_chunk += sent_text + " "
#         else:
#             chunks.append(current_chunk.strip())
#             current_chunk = (current_heading + "\n\n" if current_heading else "") + sent_text + " "

# if current_chunk:
#     chunks.append(current_chunk.strip())

# for i, chunk in enumerate(chunks):
#     print(f"\n--- Chunk {i+1} ---\n")
#     print(chunk)
