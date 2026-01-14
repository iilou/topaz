import json
from pathlib import Path
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "../../data"

INPUT_PDF = DATA_DIR / "raw" / "biochemistry_1.pdf"
OUTPUT_MD = DATA_DIR / "processed" / "chunked" / "biochemistry_1.json"

# --------------------------------
# 1. Load PDF
# --------------------------------

print(f"CONSOLE - Loading PDF from {INPUT_PDF}...")

loader = UnstructuredPDFLoader(str(INPUT_PDF), mode="elements")
docs = loader.load()

print(f"CONSOLE - Loaded {len(docs)} document(s) from {INPUT_PDF.name}")

# --------------------------------
# 2. Chunk Documents
# --------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " "]
)

print("CONSOLE - Splitting documents into chunks...")

final_chunks = []

for doc in docs:
    chunks = text_splitter.split_text(doc.page_content)
    for chunk_text in chunks:
        final_chunks.append({
            "content": chunk_text,
            "metadata": doc.metadata
        })
        
print(f"CONSOLE - Split into {len(final_chunks)} chunks.")
    
# --------------------------------
# 3. Save Chunks to JSON
# --------------------------------

with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    json.dump(final_chunks, f, indent=4)
    
print(f"CONSOLE - Saved chunks to {OUTPUT_MD}")