from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import time

import psycopg2
from psycopg2 import sql
from contextlib import contextmanager

# from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi import Depends, FastAPI, HTTPException, Request

from src.utils.process import process_query

import sys

load_dotenv()
DB_URL = os.getenv("DB_URL")

light_llm_model = "gemini-2.5-flash-lite"
prompting_llm_model = "gemini-2.5-flash"
naming_llm_model = "gemini-2.5-flash"

client = genai.Client()
collection_name = "vector_db_0"

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

def query(question: str, llm: str, cur: psycopg2.extensions.cursor, memory_size: int = 5, history_id: str | None = None) -> str:
    # response = process_query(question, llm_model=llm, client=client, collection=collection)
    response = process_query(question, cur, collection_name, client, model=llm, memory_size=memory_size, history_id=history_id, debug=False)
    return response

def create_chat_history_message(history_id: str, message: str, response: str, llm: str, user_id: str, conn: psycopg2.extensions.connection, cur: psycopg2.extensions.cursor) -> ChatHistoryItem:
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
    
    # new_history_name_prompt = """Generate a short, descriptive name for a chat history between a student and an AI biology tutor based on the student's first question. The name should be concise (3-7 words), relevant to biology, and reflect the topic of the question. Avoid generic titles; instead, focus on key terms or concepts mentioned in the question."""
    new_history_name_prompt = """Generate a descriptive name for a chat history between a student and an AI biology tutor based on the student's first question. The name should be concise (3-7 words), relevant to biology, and reflect the topic of the question. If the question is not biology-related, ignore the prompt and generate a generic name."""
    new_history_name_response = client.models.generate_content(
        model=naming_llm_model,
        contents=new_history_name_prompt + "\n\nStudent's Question: " + request.message + "\n\nChat History Name:",
        config=genai.types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=200,
        )
    )
    
    create_response = create_chat_history_if_not_exists(user_id, description="Auto-created chat history", name=new_history_name_response.text.strip())
    print(f"Created new chat history for user_id: ({user_id}): ", create_response)
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            response: str = query(request.message, request.llm, cur)
    
            chat_message: ChatHistoryItem = create_chat_history_message(create_response.history_id, request.message, response, request.llm, user_id, conn, cur)
    
    return QueryCreateResponse(
        history=create_response,
        message=chat_message
    )

# send new message
@app.post("/chat/history/{history_id}/messages", response_model=QueryAppendResponse)
def create_chat_message(request: QueryRequest, history_id: str, user_id: str = Depends(get_current_user_id)):
    print(f"-------------------- received query from user_id: ({user_id}): --------------------", request)
    
    # response = "This is a placeholder response to your question: " + request.message + " very long answer here to simulate processing. " * 50
    # time.sleep(5)
    # response = query(request.message, request.llm, 
    with get_conn() as conn:
        with conn.cursor() as cur:
            response: str = query(request.message, request.llm, cur, history_id=history_id, memory_size=20)
    
            chat_message: ChatHistoryItem = create_chat_history_message(history_id, request.message, response, request.llm, user_id, conn, cur)
    
    print(f"\n----------- created chat message for history_id: {history_id}: -----------")
    print(f"msg: {chat_message.message}")
    print(f"resp: {chat_message.response}")  # print first 100 chars
    print(f"id: {chat_message.id}")
    print(f"created_at: {chat_message.created_at}")
    print(f"llm: {chat_message.llm}")
    print("-----------------------------------------------------\n")
    
    return QueryAppendResponse(
        message=chat_message
    )


#pip install fastapi google-genai python-dotenv psycopg2-binary uvicorn spacy pgvector