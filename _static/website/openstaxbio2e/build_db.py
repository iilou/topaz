import json
from dotenv import load_dotenv

from pgvector.psycopg2 import register_vector
from pgvector import Vector
import psycopg2

import os
from pathlib import Path

from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from textbook.db import add_to_vector_database_pgvector

load_dotenv()
DB_URL = os.getenv("DB_URL")

def line_to_text_1(line):
    chunk = json.loads(line)
    # text = f"CHAPTER: {chunk.get('chapter', '')}\n\nSECTION: {chunk.get('section', '')}\n\nSUBSECTION: {chunk.get('subsection', '')}\n\nCONTENT: {chunk['text']}"
    # return text
    return chunk['text']
    # return chunk['embedding_text']

def get_metadata_1(line, textbook_name):
    chunk = json.loads(line)
    return {
        "chapter": chunk['chapter'],
        "section": chunk['section'],
        "subsection": chunk['subsection'],
        "url": chunk['url'],
        "textbook": textbook_name,
    }
    
def line_to_text_2(line):
    chunk = json.loads(line)
    return f"TERM: {chunk['term']}\n\nDEFINITION: {chunk['text']}"

def get_metadata_2(line, textbook_name):
    chunk = json.loads(line)
    metadata = {
        "term": chunk['term'],
        "source": chunk['source'],
        "url": chunk['url'],
        "textbook": textbook_name,
    }
    return metadata

def add_to_db(jsonl_path, collection, textbook_name, embedded_text_fn=line_to_text_1, metadata_fn=get_metadata_1):
    
    with open(jsonl_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    print(f"Starting embedding for {len(lines)} lines...")
    
    docs = []
    
    for i, line in enumerate(lines):
        chunk = json.loads(line)
        
        text = embedded_text_fn(line)
        metadata = metadata_fn(line, textbook_name)
        
        doc = Document(page_content=text, metadata=metadata)
        docs.append(doc)
        
        if (i + 1) % 100 == 0:
            print(f"Prepared {i + 1} / {len(lines)} documents...")
            
    add_to_vector_database_pgvector(collection, docs, DB_URL, textbook_name)
    


# CHANGE THESE
PARAGRAPHS_JSONL_PATH = "website/openstaxbio2e/biology_mvp_chunkedv2.jsonl"
KEYTERMS_JSONL_PATH = "biology_glossary.jsonl"
TEXTBOOK_NAME = "biology-2e"

# MOSTLY CONSISTENT
PARAGRAPHS_COLLECTION_NAME = "vector_db_0"
KEYTERMS_COLLECTION_NAME = "vector_db_0"

# PROBABLY WON'T CHANGE
# CHROMA_DB_PATH = "vector_db"

add_to_db(PARAGRAPHS_JSONL_PATH, PARAGRAPHS_COLLECTION_NAME, TEXTBOOK_NAME, line_to_text_1, get_metadata_1)
# add_to_db(KEYTERMS_JSONL_PATH, KEYTERMS_COLLECTION_NAME, TEXTBOOK_NAME, line_to_text_2, get_metadata_2)