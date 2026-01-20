from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import time

import psycopg2
from psycopg2 import sql
from contextlib import contextmanager

from fastapi import Depends, FastAPI, HTTPException, Request

from src.utils.process import process_query

import sys

load_dotenv()
DB_URL = os.getenv("DB_URL")

light_llm_model = "gemini-2.0-flash-lite"
prompting_llm_model = "gemini-2.5-flash"

client = genai.Client()
collection_name = "biology_paragraphs"

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
    return {"message": "backend is running", "status": "ok"}

class ChatHistory(BaseModel):
    user_id: str
    description: str
    created_at: str
    history_id: str
    name: str
    
class ChatHistoryItem(BaseModel):
    message: str
    response: str
    created_at: str
    id: str
    llm: str
    
class QueryRequest(BaseModel):
    llm: str
    message: str
    
class QueryCreateResponse(BaseModel):
    history: ChatHistory
    message: ChatHistoryItem
    
class QueryAppendResponse(BaseModel):
    message: ChatHistoryItem


def get_current_user_id(request: Request) -> str:
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user_id




@app.get("/chat/histories")
def get_chat_histories(user_id: str = Depends(get_current_user_id)):
    with get_conn() as conn:
        with conn.cursor() as cur:
            select_query = sql.SQL("""
                SELECT id, description, created_at, name
                FROM chat_history
                WHERE user_id = %s
                ORDER BY created_at DESC
            """)
            cur.execute(select_query, (user_id,))
            rows = cur.fetchall()
    
    histories = [
        ChatHistory(
            user_id=user_id,
            description=row[1] or "",
            created_at=row[2].isoformat(),
            history_id=row[0],
            name=row[3] or ""
        )
        for row in rows
    ]
    
    print(f"Histories fetched for userid: ({user_id})", histories)
    
    return histories

@app.get("/chat/history/{history_id}/messages")
def get_chat_history_messages(history_id: str):
    print(f"Fetching messages for history_id: {history_id}")
    with get_conn() as conn:
        with conn.cursor() as cur:
            select_query = sql.SQL("""
                SELECT message, response, created_at, id, llm
                FROM chat_history_message
                WHERE history_id = %s
                ORDER BY created_at ASC
            """)
            cur.execute(select_query, (history_id,))
            rows = cur.fetchall()
    
    messages = [
        ChatHistoryItem(
            message=row[0],
            response=row[1],
            created_at=row[2].isoformat(),
            id=row[3],
            llm=row[4]
        )   
        for row in rows
    ]
    
    print(f"Messages fetched for history_id: ({history_id})", messages)
    
    return messages

# return certain columns
def create_chat_history_if_not_exists(user_id: str, name, description: str = "") -> ChatHistory:
    with get_conn() as conn:
        with conn.cursor() as cur:
            insert_query = sql.SQL("""
                INSERT INTO chat_history (user_id, description, name)
                VALUES (%s, %s, %s)
                RETURNING id, name, created_at, user_id, description
            """)
            cur.execute(insert_query, (user_id, description, name))
            returned = cur.fetchone()
            conn.commit()
            
    return ChatHistory(
        user_id=returned[3],
        description=returned[4] or "",
        created_at=returned[2].isoformat(),
        history_id=returned[0],
        name=returned[1]
    )

def query(question: str, llm: str, cur: psycopg2.extensions.cursor) -> str:
    # response = process_query(question, llm_model=llm, client=client, collection=collection)
    response = process_query(question, cur, "biology_paragraphs", client, model=llm, debug=False)
    return response

def create_chat_history_message(history_id: str, message: str, response: str, llm: str, user_id: str) -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            insert_query = sql.SQL("""
                INSERT INTO chat_history_message (history_id, message, response, llm, user_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, created_at
            """)
            cur.execute(insert_query, (history_id, message, response, llm, user_id))
            returned = cur.fetchone()
            conn.commit()

    return ChatHistoryItem(
        message=message,
        response=response,
        created_at=returned[1].isoformat(),
        id=str(returned[0]),
        llm=llm
    )
    

@app.post("/chat/history/messages", response_model=QueryCreateResponse)
def create_chat_message_no_history(request: QueryRequest, user_id: str = Depends(get_current_user_id)):
    print(f"Received query from user_id: ({user_id}): ", request)
    
    create_response = create_chat_history_if_not_exists(user_id, description="Auto-created chat history", name="New Chat")
    print(f"Created new chat history for user_id: ({user_id}): ", create_response)
    
    response = "This is a placeholder response to your question: " + request.message
    time.sleep(5)
    # response = query(request.message, request.llm)
    
    chat_message = create_chat_history_message(create_response.history_id, request.message, response, request.llm, user_id)
    print(f"Created chat message for history_id: {create_response.history_id}: ", chat_message)
    
    return QueryCreateResponse(
        history=create_response,
        message=chat_message
    )

# send new message
@app.post("/chat/history/{history_id}/messages", response_model=QueryAppendResponse)
def create_chat_message(request: QueryRequest, history_id: str, user_id: str = Depends(get_current_user_id)):
    print(f"Received query from user_id: ({user_id}): ", request)
    
    response = "This is a placeholder response to your question: " + request.message + " very long answer here to simulate processing. " * 50
    time.sleep(5)
    # response = query(request.message, request.llm)
    
    chat_message = create_chat_history_message(history_id, request.message, response, request.llm, user_id)
    print(f"Created chat message for history_id: {history_id}: ", chat_message)
    
    return QueryAppendResponse(
        message=chat_message
    )


#pip install fastapi google-genai python-dotenv psycopg2-binary uvicorn spacy pgvector