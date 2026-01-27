from google import genai
from dotenv import load_dotenv
import os
from pathlib import Path

import psycopg2
from psycopg2 import sql
from pgvector.psycopg2 import register_vector
from pgvector import Vector

from .retrieve import retrieve_docs

def gate_rag_access(message: str, client: genai.Client, debug: bool = False) -> bool:
    system_instructions = (
        "You are an AI assistant that determines whether a user's question requires access to external textbook resources. "
        "If the question is about biology concepts, textbook content, or requires detailed explanations, respond with 'YES'. "
        "If the question is general knowledge, personal advice, or unrelated to biology, respond with 'NO'. "
        "Only respond with 'YES' or 'NO'."
    )

    user_message = f"""QUESTION:
{message}
Does this question require access to external textbook resources to provide an accurate answer? Respond with 'YES' or 'NO'."""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=genai.types.GenerateContentConfig(
            temperature=0.0,
            max_output_tokens=50,
            system_instruction=system_instructions,
        ),
        contents=user_message
    )
    
    # if debug:
    print(f"Gating RAG access response: {response.text} | for question: {message}")
    
    answer = response.text.strip().upper()
    return answer == "YES"

def process_query(message: str, cur: psycopg2.extensions.cursor, collection: str, client: genai.Client, model: str, memory_size: int = 5, history_id: str | None = None, debug=False) -> str:
    # retrieved_docs = retrieve_docs(message, collection, client, k=5, threshold=0.8)
        
    context_blocks = ""
    
    if history_id and memory_size > 0:
        sql_query = sql.SQL("""
            SELECT message, response
            FROM chat_history_message
            WHERE history_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        """)
        cur.execute(sql_query, (history_id, memory_size))
        history_rows = cur.fetchall()
        
        if debug:
            print(f"--- Retrieved {len(history_rows)} history rows ---")
            print(history_rows)
        
        if history_rows:
            context_blocks += f"\n\n--- STUDENT-TEACHER PREVIOUS INTERACTIONS (ORDERED MOST RECENT FIRST, LIMIT OF {memory_size}) ---\n"
            for i, row in enumerate(history_rows):
                prev_message = row[0]
                prev_response = row[1]
                context_blocks += f"\n--- PRIOR EXCHANGE #{i+1} ---\n"
                context_blocks += f"STUDENT: {prev_message}\n"
                context_blocks += f"TUTOR: {prev_response}\n"
    
    is_needs_rag = gate_rag_access(message, client, debug=debug)
    
    if debug:
        print(f"--- RAG NEEDED: {is_needs_rag} ---")
        
    if not is_needs_rag:
        # direct generation without retrieval
        if debug:
            print(f"--- DIRECT GENERATION WITHOUT RETRIEVAL ---")
        
        system_instructions = (
            "You are an AI biology tutor helping a student understand core biological concepts. "
            "This question is not related to biology, so you do not have immediate access to textbook exerpts. "
            "However in the situation that the user asks a biology-related question, you will have access to textbook context to answer questions accurately and clearly. "
            "The topics you would have access to include genetics, biochemistry, molecular biology, cell biology, and related fields. "
            "The level of these textbook range from high school to early undergraduate. "
        )
        user_message = f"""PREVIOUS INTERACTIONS:
{context_blocks}
QUESTION:
{message}
Provide a clear, student-friendly explanation:"""
        
        if debug:
            print(f"--- FINAL PROMPT ---")
            print(user_message)
        response = client.models.generate_content(
            model=model,
            config=genai.types.GenerateContentConfig(
                temperature=1.5,
                max_output_tokens=4000,
                system_instruction=system_instructions,
            ),
            contents=user_message
        )
        
        return response.text
    
    res = retrieve_docs(message, cur, collection, client, k=25, n=5, debug=debug)

    for i, row in enumerate(res):
        # doc, metadata, distance = row[0], row[1], row[2]
        doc = row[0]
        
        context_blocks += f"\n--- EXCERPT {i+1} ---\n"
        context_blocks += f"{doc}\n"
        
    if debug:
        print(f"--- CONTEXT BLOCKS (prev) ---")
        print(context_blocks[:200])
        

    
    
    # for i, item in enumerate(retrieved_docs):
    #     header = item['metadata'].get('Header 2', 'General Section')
    #     context_blocks += f"\n--- EXCERPT {i+1} (Source: {header}) ---\n"
    #     context_blocks += f"{item['document']}\n"

    system_instructions = (
        "You are an AI biology tutor helping a student understand core biological concepts. "
        "Use the provided textbook context to answer questions accurately and clearly. "
        "You are given previous student-tutor interactions to maintain context up to a limit. "
        "Synthesize information across the context when appropriate. "
        "Do not introduce facts that are not supported by the context. "
        "Do not explicitly reference the excerpts in your answer. "
        "If the context is insufficient to fully answer the question, state that explicitly."
    )

    user_message = f"""CONTEXT:
{context_blocks}

QUESTION:
{message}

Provide a clear, student-friendly explanation:"""
    
    if debug:
        print(f"--- FINAL PROMPT ---")
        print(user_message)

    response = client.models.generate_content(
        model=model,
        config=genai.types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=8000,
            system_instruction=system_instructions,
        ),
        contents=user_message
    )
    
    if debug:
        print(f"--- RESPONSE ---")
        print(response.text)

    return response.text



def wfwefwe():
    load_dotenv()

    DB_URL = os.getenv("DB_URL")
    
    client = genai.Client()
    
    conn = psycopg2.connect(DB_URL, sslmode='require')
    register_vector(conn)
    cur = conn.cursor()
    k = 5
    threshold = 0.9
    
    # biochemistry example
    query = "What are the primary functions of DNA polymerase?"
    results = process_query(query, cur, "vector_db_0", client, model="gemini-2.5-flash", debug=True)
    
    # genetics example
    query = "What is the role of mRNA in protein synthesis?"
    results = process_query(query, cur, "vector_db_0", client, model="gemini-2.5-flash", debug=False)
    print("res: ", results)
    
# wfwefwe()