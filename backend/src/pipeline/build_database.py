import json
import chromadb
from google import genai
from google.genai import types
from dotenv import load_dotenv
import numpy as np

load_dotenv()

client = genai.Client()

def add_to_vector_database(json_chunks_path, chroma_db_path, collection_name, specific_collection_name):
    db_client = chromadb.PersistentClient(path=chroma_db_path)
    collection = db_client.get_or_create_collection(name=collection_name)
    collection_specific = db_client.get_or_create_collection(name=specific_collection_name)
    
    with open(json_chunks_path, "r") as f:
        chunks = json.load(f)
        
    print(f"Starting embedding for {len(chunks)} chunks...")
    
    for chunk in chunks:
        # embed
        result = client.models.embed_content(
            model="text-embedding-004",
            contents=chunk["embedding_text"],
            # contents=chunk["content"],
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
        )
        
        vector = result.embeddings[0].values
        v = np.array(vector)
        v = v / np.linalg.norm(v)  # normalize

        collection.add(
            ids=[str(chunk["id"])],
            embeddings=[v.tolist()],
            documents=[chunk["content"]],
            metadatas=[chunk["metadata"]],
        )
        
        collection_specific.add(
            ids=[str(chunk["id"])],
            embeddings=[v.tolist()],
            documents=[chunk["content"]],
            metadatas=[chunk["metadata"]],
        )