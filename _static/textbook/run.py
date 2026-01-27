from clean_docs import clean_textbook_docs
from chunk_docs import chunk_textbook_docs
from load_docs import convert_textbook_to_langchain_docs
# from db_local_chroma import add_to_vector_database
from db import add_to_vector_database_pgvector

from dotenv import load_dotenv

import os

load_dotenv()

debug_logs = []

def run_textbook_pipeline(config):
    docs = convert_textbook_to_langchain_docs(config["textbook_path"], debug_logs)
    
    with open("loaded_docs_debug.txt", "w", encoding="utf-8") as f:
        for i, doc in enumerate(docs):
            f.write(f"--- Document {i} ---\n")
            f.write(doc.page_content + "\n\n")
            f.write(f"Metadata: {doc.metadata}\n\n" )
    
    cleaned_docs = clean_textbook_docs(docs, config["cleaning_preset"], debug_logs)
    
    with open("cleaned_docs_debug.txt", "w", encoding="utf-8") as f:
        for i, doc in enumerate(cleaned_docs):
            f.write(f"--- Document {i} ---\n")
            f.write(doc.page_content + "\n\n")
            f.write(f"Metadata: {doc.metadata}\n\n" )
    
    chunked_docs = chunk_textbook_docs(cleaned_docs, config["chunk_size"], config["chunk_overlap"], debug_logs)
    
    with open("chunked_docs_debug.txt", "w", encoding="utf-8") as f:
        for i, doc in enumerate(chunked_docs):
            f.write(f"--- Chunk {i} ---\n")
            f.write(doc.page_content + "\n\n")
            f.write(f"Metadata: {doc.metadata}\n\n")
    
    # add_to_vector_database(
    #     chroma_db_path=config["chroma_db_path"],
    #     collection_name=config["collection_name"],
    #     docs=chunked_docs,
    # )
    add_to_vector_database_pgvector(table_name=config["table_name"], docs=chunked_docs, db_url=config["pgvector_db_url"], label=config["label"])
    
    with open("debug_logs.txt", "w", encoding="utf-8") as f:
        for log in debug_logs:
            f.write(log + "\n")

config_1 = {
    "textbook_path": "textbook/raw/genetics_1.pdf",
    "cleaning_preset": "genetics_1",
    "pgvector_db_url": os.getenv("DB_URL"),
    "table_name": "vector_db_0",
    "label": "genetics_1",
    "chunk_size": 1200,
    "chunk_overlap": 400,
}

config_2 = {
    "textbook_path": "textbook/raw/biochemistry_1.pdf",
    "cleaning_preset": "biochemistry_1",
    "pgvector_db_url": os.getenv("DB_URL"),
    "table_name": "vector_db_0",
    "label": "biochemistry_1",
    "chunk_size": 1200,
    "chunk_overlap": 400,
}

if __name__ == "__main__":
    run_textbook_pipeline(config_1)
    run_textbook_pipeline(config_2)