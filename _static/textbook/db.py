from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings

from pgvector.psycopg2 import register_vector
from pgvector import Vector
from psycopg2.extras import execute_values, Json
import psycopg2

from langchain_core.documents import Document

import os

def add_to_vector_database_pgvector(table_name: str, docs: list[Document], db_url: str, label: str) -> None:
    """
    Adds a list of Document objects to a PostgreSQL database table with pgvector support.
    Each document is embedded using the "text-embedding-004" model, and the resulting vector,
    along with the document content and metadata, is stored in the specified table.
    Args:
        table_name (str): Name of the database table to add documents to.
        docs (list[Document]): List of Document objects to be embedded and stored.
        db_url (str): Database connection URL.
    Raises:
        Any exceptions raised by the database client or embedding model will propagate.
    """
    print("-------------------------------------------------")
    print(f"Adding {len(docs)} documents to PostgreSQL table '{table_name}'...")
    
    conn = psycopg2.connect(db_url, sslmode='require')
    register_vector(conn)
    cur = conn.cursor()
    
    # batch insert
    embeddings = GoogleGenerativeAIEmbeddings(model="text-embedding-004", google_api_key=os.getenv("GOOGLE_API_KEY"))
    
    texts = [doc.page_content for doc in docs]
    vectors = embeddings.embed_documents(texts)
    
    assert all (len(vector) == 768 for vector in vectors), "Embedding vector size mismatch."
    
    print(f"Embedded {len(vectors)} documents, inserting into database...")
    
    rows = [
        (Vector(vector), doc.page_content, Json(doc.metadata), label, False, 0)
        for vector, doc in zip(vectors, docs)
    ]
    
    execute_values(
        cur,
        f"""INSERT INTO {table_name} (embedding, content, metadata, label, is_validated, score) VALUES %s""",
        rows
    )

    conn.commit()
    cur.close()
    print("Finished embedding and adding to database.")
    print("-------------------------------------------------\n")