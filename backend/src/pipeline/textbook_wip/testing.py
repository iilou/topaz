import pypdf
from pypdf import PdfReader

import re

def remove_blurbs(text):
    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if re.fullmatch(r"[✷•*–—\-]+", line):
            continue
        
        if re.match(r"^(Figure|Table)\s*\d+", line):
            continue

        if len(line.split()) <= 4 and line.isupper():
            continue

        if re.fullmatch(r"\d+", line):
            continue

        cleaned_lines.append(line)

    # Re-join lines, preserving paragraph breaks (double newline)
    cleaned_text = "\n".join(cleaned_lines)

    # Fix hyphenated words across line breaks
    cleaned_text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", cleaned_text)

    return cleaned_text


reader = PdfReader("data/raw/genetics_1.pdf")

full_text = ""
for page in reader.pages:
    full_text += page.extract_text() + "\n\n"
    
full_text = remove_blurbs(full_text)
    
with open("data/processed/markdown/genetics_1adf.md", "w", encoding="utf-8") as f:
    f.write(full_text)