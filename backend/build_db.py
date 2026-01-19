import json
import chromadb
from google import genai
from google.genai import types
from dotenv import load_dotenv
import numpy as np

load_dotenv()
client = genai.Client()

def line_to_text_1(line):
    chunk = json.loads(line)
    # text = f"CHAPTER: {chunk.get('chapter', '')}\n\nSECTION: {chunk.get('section', '')}\n\nSUBSECTION: {chunk.get('subsection', '')}\n\nCONTENT: {chunk['text']}"
    # return text
    # return chunk['text']
    return chunk['embedding_text']

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

def add_to_db(jsonl_path, chroma_db_path, collection_name, textbook_name, embedded_text_fn=line_to_text_1, metadata_fn=get_metadata_1):
    db_client = chromadb.PersistentClient(path=chroma_db_path)
    collection = db_client.get_or_create_collection(name=collection_name)
    
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
        
        collection.add(
            ids=[str(i)],
            embeddings=[vector],
            metadatas=[metadata_fn(line, textbook_name)],
            # documents=[chunk["embedding_text"]]
            documents=embedded_text_fn(line),
        )
        
    print("Finished embedding and adding to database.")


# CHANGE THESE
PARAGRAPHS_JSONL_PATH = "biology_mvp_chunked.jsonl"
KEYTERMS_JSONL_PATH = "biology_glossary.jsonl"
TEXTBOOK_NAME = "biology-2e"

# MOSTLY CONSISTENT
PARAGRAPHS_COLLECTION_NAME = "biology_paragraphs"
KEYTERMS_COLLECTION_NAME = "biology_keyterms"

# PROBABLY WON'T CHANGE
CHROMA_DB_PATH = "vector_db"

add_to_db(PARAGRAPHS_JSONL_PATH, CHROMA_DB_PATH, PARAGRAPHS_COLLECTION_NAME, TEXTBOOK_NAME, line_to_text_1, get_metadata_1)
add_to_db(KEYTERMS_JSONL_PATH, CHROMA_DB_PATH, KEYTERMS_COLLECTION_NAME, TEXTBOOK_NAME, line_to_text_2, get_metadata_2)