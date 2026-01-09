import requests
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
import chromadb

from contextlib import asynccontextmanager
from fastapi import FastAPI

from .utils.retrieve import retrieve_docs

load_dotenv()

light_llm_model = "gemini-2.0-flash-lite"
prompting_llm_model = "gemini-2.0-flash"

obj = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    obj['client'] = genai.Client()
    obj['db_client'] = chromadb.PersistentClient(path="./genetics_db")
    obj['collection'] = obj['db_client'].get_or_create_collection(name="genetics_textbook")
    yield
    
    obj.clear()
    
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "backend is running", "document_count": obj['collection'].count()}

