import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
import numpy as np

from pgvector.psycopg2 import register_vector
from pgvector import Vector
import psycopg2

import os
from pathlib import Path

load_dotenv()
client = genai.Client()
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
    
    conn = psycopg2.connect(DB_URL, sslmode='require')
    register_vector(conn)
    cur = conn.cursor()
    
    with open(jsonl_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    print(f"Starting embedding for {len(lines)} lines...")
    
    for i, line in enumerate(lines):
        chunk = json.loads(line)
        
        # embed
        result = client.models.embed_content(
            model="text-embedding-004",
            contents=embedded_text_fn(line),
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
        )
        
        vector = result.embeddings[0].values
        vector_obj = Vector(vector)
        
        # add to Postgres
        cur.execute(
            f"""
            INSERT INTO {collection} (embedding, content, metadata)
            VALUES (%s, %s, %s)
            """,
            (
                vector_obj,
                embedded_text_fn(line),
                json.dumps(metadata_fn(line, textbook_name))
            )
        )
        if (i + 1) % 100 == 0:
            conn.commit()
            print(f"---- EMBEDDED i_{i+1} to i_{i+100} ----")
            
    conn.commit()
    cur.close()
        
    print("Finished embedding and adding to database.")


# CHANGE THESE
PARAGRAPHS_JSONL_PATH = "biology_mvp_chunkedv2.jsonl"
KEYTERMS_JSONL_PATH = "biology_glossary.jsonl"
TEXTBOOK_NAME = "biology-2e"

# MOSTLY CONSISTENT
PARAGRAPHS_COLLECTION_NAME = "biology_paragraphs"
KEYTERMS_COLLECTION_NAME = "biology_keyterms"

# PROBABLY WON'T CHANGE
# CHROMA_DB_PATH = "vector_db"

add_to_db(PARAGRAPHS_JSONL_PATH, PARAGRAPHS_COLLECTION_NAME, TEXTBOOK_NAME, line_to_text_1, get_metadata_1)
# add_to_db(KEYTERMS_JSONL_PATH, KEYTERMS_COLLECTION_NAME, TEXTBOOK_NAME, line_to_text_2, get_metadata_2)