import requests
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
import chromadb
import os

import psycopg2
from psycopg2 import sql
from contextlib import contextmanager

from contextlib import contextmanager
from fastapi import FastAPI

from src.utils.process import process_query

load_dotenv()
DB_URL = os.getenv("DB_URL")

light_llm_model = "gemini-2.0-flash-lite"
prompting_llm_model = "gemini-2.0-flash"

client = genai.Client()
db_client = chromadb.PersistentClient(path="./vector_db")
collection = db_client.get_or_create_collection(name="biology_paragraphs")

@contextmanager
def get_conn():
    conn = psycopg2.connect(DB_URL, sslmode='require', connect_timeout=10)
    try:
        yield conn
    finally:
        conn.close()
    
app = FastAPI()

@app.get("/")
def root():
    return {"message": "backend is running", "document_count": collection.count()}



# @app.post("/chat")
# async def chat_endpoint(request: ChatRequest):
#     question = request.question
    
#     # placeholder for llm call
#     response = "This is a placeholder response to your question: " + question
    
#     return {"answer": response}


class QueryRequest(BaseModel):
    question: str
    user_id: str
    history_id: str | None = None
    
class QueryResponse(BaseModel):
    answer: str
    created_at: str

class ChatHistory(BaseModel):
    user_id: str
    description: str
    created_at: str
    history_id: str
    
# queryrequest
@app.post("/query")
def query_endpoint(request: QueryRequest):
    response = process_query(
        message=request.question,
        db_client=db_client,
        collection=collection,
        client=client,
        model=prompting_llm_model,
    )
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            insert_query = sql.SQL("""
                INSERT INTO chat_histories (user_id, question, answer)
                VALUES (%s, %s, %s)
                RETURNING history_id, created_at
            """)
            cur.execute(insert_query, (request.user_id, request.question, response))
            response = cur.fetchone()
            conn.commit()

    result = QueryResponse(
        answer=response,
        created_at=response[1]
    )
    
    return result