from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
import json
import re

def chunk_md(path, output_json):
    with open(path, "r", encoding="utf-8") as f:
        md_text = f.read()
        
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    sections = header_splitter.split_text(md_text)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " "]
    )

    final_chunks = text_splitter.split_documents(sections)


    def make_embedding_text(chunk):
        text = chunk.page_content

        # remove LaTeX blocks
        text = re.sub(r"\$\$.*?\$\$", "", text, flags=re.DOTALL)

        # collapse tables into a short description
        text = re.sub(r"\n\|.*?\|\n", "\n[Table present]\n", text)

        # remove citation clutter
        text = re.sub(r"\[\d+\]", "", text)

        return text

    # 4. Save chunks to a JSON file for your RAG pipeline
    output_data = []
    for i, chunk in enumerate(final_chunks):
        #check if metadata is a blank dict
        if not chunk.metadata:
            chunk.metadata = {"source": "unknown"}
        
        output_data.append({
            "id": i,
            "content": chunk.page_content,
            "metadata": chunk.metadata,
            "embedding_text": make_embedding_text(chunk)
        })

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4)