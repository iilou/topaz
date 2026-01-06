import json
import chromadb
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# 1. Setup Gemini Client
# Make sure you have: pip install google-genai
client = genai.Client()

# 2. Setup Persistent ChromaDB
# This creates the 'genetics_db' folder on your hard drive
db_client = chromadb.PersistentClient(path="./genetics_db")
collection = db_client.get_or_create_collection(name="genetics_textbook")

# 3. Load your JSON chunks
with open("genetics_chunks.json", "r") as f:
    chunks = json.load(f)

print(f"Starting embedding for {len(chunks)} chunks...")

# 4. Embed and Store
for chunk in chunks:
    # Generate the vector
    result = client.models.embed_content(
        model="text-embedding-004",
        contents=chunk["content"],
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )
    
    # Static vector extracted from the API response
    vector = result.embeddings[0].values

    # Add to ChromaDB
    collection.add(
        ids=[str(chunk["id"])],
        embeddings=[vector],
        documents=[chunk["content"]],
        metadatas=[chunk["metadata"]]
    )

print("Done! Your genetics_db folder is now populated with static vectors.")