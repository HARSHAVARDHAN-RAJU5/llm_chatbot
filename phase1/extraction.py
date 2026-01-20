from PyPDF2 import PdfReader
import re

# Load PDF
reader = PdfReader("python2.pdf")

# Extract raw text
raw_text = ""
for page in reader.pages:
    raw_text += page.extract_text() + "\n"

# Normalize newlines
text = raw_text.replace("\r", "\n")

# Preserve paragraph breaks (2+ newlines)
text = re.sub(r"\n{2,}", "\n\n", text)

# Replace single newlines with spaces
text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

# Collapse multiple spaces
text = re.sub(r"[ ]{2,}", " ", text)

# Known headings
headings = [
    "Introduction",
    "Advantages of Learning Python",
    "Indentation in Python",
    "Print Function",
    "Variables",
    "Python Operators",
    "Keyword",
    "Data Type",
    "Conditional Statements in Python",
    "Loops in Python",
    "Functions",
    "Python Functions",
    "Python pass Statement",
    "Global and Local Variables in Python",
    "Data Structures",
    "OOP Concepts",
    "Python OOP"
]

# Force headings onto their own lines
for h in headings:
    text = re.sub(rf"\s*{re.escape(h)}\s*", f"\n\n{h}\n", text)

# Fix bullet points
text = text.replace(" ● ", "\n• ")

# Clean excessive newlines
text = re.sub(r"\n{3,}", "\n\n", text)

print(text)
