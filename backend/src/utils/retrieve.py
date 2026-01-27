from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from pathlib import Path

from pgvector.psycopg2 import register_vector
from pgvector import Vector
import psycopg2
from psycopg2 import sql

from .rerank import rerank_results


def retrieve_docs(query: str, cur: psycopg2.extensions.cursor, collection: str, client: genai.Client, k: int, n: int, rerank=True, debug: bool = False) -> list[str]:
    """Retrieve relevant documents from the ChromaDB based on the query."""
    print(f"\n\n----------- retrieving docs for query: {query}")
    
    # generate embedding from gemini
    query_embedding_res = client.models.embed_content(
        model="text-embedding-004",
        contents=query,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
    )
    query_vector = query_embedding_res.embeddings[0].values

    # search vector db
    sql_query = sql.SQL("""
        SELECT content, metadata, distance, is_validated, score
        FROM (
            SELECT content, metadata, embedding <-> %s::vector AS distance, is_validated, score
            FROM {table}
        ) t
        ORDER BY distance
        LIMIT %s;
    """).format(table=sql.Identifier(collection))

    cur.execute(
        sql_query,
        (query_vector, k)
    )
    rows = cur.fetchall()
        
    if rerank:
        print(f"Reranking retrieved documents...")
        reranked_content = rerank_results(query, [row[0] for row in rows])
        
        # relavence_scores = [reranked_content["data"][i]["relevance_score"] for i in range(len(reranked_content["data"]))]
        # index = [reranked_content["data"][i]["index"] for i in range(len(reranked_content["data"]))]
        
        if debug:
            print(f"--- RERANKED RESULTS ---")
            for idx, ranked in enumerate(reranked_content["data"]):
                print(f"----------------------------")
                print(f"Rank {idx+1}:")
                print(f"Index in original results: {ranked['index']}")
                print(f"Relevance Score: {ranked['relevance_score']}")
                print(f"Document Content: {ranked['document']}")
            print(f"----------------------------\n")
            
        # rearrange rows based on reranked indices
        rows = [rows[ranked['index']] + (ranked['relevance_score'],) for ranked in reranked_content["data"]]
            
        
    
    # debug print
    if debug:
        print(f"--- RETRIVAL RESULTS ---")
        for i, row in enumerate(rows):
            print(f"------------------- res {i+1} -------------------")
            print(f"doc: {row[0]}")
            print(f"metadata: {row[1]}")
            print(f"distance: {row[2]}")
            print(f"is_validated: {row[3]}")
            print(f"score: {row[4]}")
            if rerank:
                print(f"relevance_score: {row[5]}")
            print("\n")
        print(f"-------------------------\n")
    
    # return top n results
    return rows[:n]

# test function
def testasdffs(rerank: bool = False):
    load_dotenv()

    DB_URL = os.getenv("DB_URL")
    
    client = genai.Client()
    
    conn = psycopg2.connect(DB_URL, sslmode='require')
    register_vector(conn)
    cur = conn.cursor()
    k = 20
    
    # biochemistry example
    query = "What are the primary functions of DNA polymerase?"
    results = retrieve_docs(query, cur, "vector_db_0", client, k, debug=True)
    
    # genetics example
    query = "What is the role of mRNA in protein synthesis?"
    results = retrieve_docs(query, cur, "vector_db_0", client, k, debug=True)
    
    #rerank test
    # if rerank:
    #     reranked_content = rerank_results(query, [row[0] for row in results])
    #     print(f"Reranked Documents:")
    #     for i, ranked in enumerate(reranked_content["data"][:5]):
    #         print(f"--- Reranked Document {i+1} ---")
    #         print(ranked)
    #         print("\n")
            
    #     # return top 5 reranked
    #     return reranked_content["data"][:5]
    
# testasdffs(True)
    
    
    
#     db_client = chromadb.PersistentClient(path=path_vector_db)
#     # collection = db_client.get_or_create_collection(name="genetics_textbook")
#     collection = db_client.get_collection(name="biology_paragraphs")
#     collection_2 = db_client.get_collection(name="biology_keyterms")

#     # biochemistry example
#     query = "What are the primary functions of DNA polymerase?"
#     # genetics example
#     # query = "What is the role of mRNA in protein synthesis?"
#     # cell biology example
#     # query = "Describe the structure and function of the mitochondrion."
#     # physiology example
#     # query = "Explain the process of muscle contraction."
#     k = 5

#     results = retrieve_docs(query, collection, client, k=k, threshold=0.8)
#     results2 = retrieve_docs(query, collection_2, client, k=k, threshold=0.8)

#     for i in range(k):
#         print(f"Document {i+1}:")
#         print(f"Content: {results[i]['document']}")
#         print(f"Distance: {results[i]['dist']:.4f}")
#         print(f"Metadata: {results[i]['metadata']}")
#         print()
        
#     for i in range(k):
#         print(f"Keyterm {i+1}:")
#         print(f"Content: {results2[i]['document']}")
#         print(f"Distance: {results2[i]['dist']:.4f}")
#         print(f"Metadata: {results2[i]['metadata']}")
#         print()

# # testasdffs()