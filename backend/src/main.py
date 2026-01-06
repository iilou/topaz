import requests
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
import chromadb

from contextlib import asynccontextmanager
from fastapi import FastAPI

from .utils.retrieve import retrieve_docs

load_dotenv()

client = genai.Client()
light_llm_model = "gemini-2.0-flash-lite"
prompting_llm_model = "gemini-2.0-flash"

# reponse = client.models.generate_content(
#     model=light_llm_model, contents="Hi again! Just testing for now, giving you some prompts later :)"
# )

db_client = chromadb.PersistentClient(path="./genetics_db")
collection = db_client.get_or_create_collection(name="genetics_textbook")

