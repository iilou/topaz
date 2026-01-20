import re

def clean_markdown(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove Table of Contents (usually messy and confuses RAG)
    # This looks for the "Contents" header and removes until the first real Chapter
    content = re.sub(
        r"## Contents[\s\S]*?##\s+Chapter\s+1",
        "## Chapter 1",
        content,
        flags=re.IGNORECASE
    )

    # 2. Remove Page Numbers
    # Matches a newline followed by a digit and a newline (common at bottom of pages)
    content = re.sub(r"\n\d+\s*\n", "\n\n", content)
    
    # 3. Fix common Biology OCR symbol errors (from your previous output)
    replacements = {
        " \u00b5": " micrometers", # Fixes µ symbol
        " \u00c5": " Angstroms",   # Fixes Å symbol
        "1 \u2013 3": "1-3",       # Fixes dash
        "E . c coli": "E. coli",   # Fixes the common E. coli typo
    }
    for bad, good in replacements.items():
        content = content.replace(bad, good)
    
    content = content.replace("", "")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Markdown cleaned successfully!")
