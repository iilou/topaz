from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
import json

# 1. Load your Markdown file
file_path = "genetics_clean.md"
with open(file_path, "r", encoding="utf-8") as f:
    md_text = f.read()

# 2. Split by Section Headers (Structural Chunking)
# This ensures "Chapter 1" content stays categorized under "Chapter 1"
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
sections = header_splitter.split_text(md_text)

# 3. Further split large sections (Recursive Chunking)
# 1500 chars is the 'sweet spot' for Biology to keep full definitions intact
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " "]
)

final_chunks = text_splitter.split_documents(sections)

# 4. Save chunks to a JSON file for your RAG pipeline
output_data = []
for i, chunk in enumerate(final_chunks):
    output_data.append({
        "id": i,
        "content": chunk.page_content,
        "metadata": chunk.metadata
    })

with open("genetics_chunks.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=4)

print(f"Success! Created {len(output_data)} chunks.")