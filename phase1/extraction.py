from PyPDF2 import PdfReader
import re

reader = PdfReader("python2.pdf")

raw_text = ""
for page in reader.pages:
    raw_text += page.extract_text() + "\n"

text = raw_text.replace("\r", "\n")

text = re.sub(r"\n{2,}", "\n\n", text)

text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

text = re.sub(r"[ ]{2,}", " ", text)

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

for h in headings:
    text = re.sub(rf"\s*{re.escape(h)}\s*", f"\n\n{h}\n", text)

text = text.replace(" ● ", "\n• ")

text = re.sub(r"\n{3,}", "\n\n", text)

print(text)

with open("clean_text.txt", "w", encoding="utf-8") as f:
    f.write(text)
