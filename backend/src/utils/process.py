from google import genai
import chromadb
from dotenv import load_dotenv
import os
from pathlib import Path

from retrieve import retrieve_docs


def process_query(message: str, db_client: chromadb.PersistentClient, collection: chromadb.Collection, client: genai.Client, model: str) -> str:
    retrieved_docs = retrieve_docs(message, collection, client, k=5, threshold=0.8)

    context_blocks = ""
    for i, item in enumerate(retrieved_docs):
        header = item['metadata'].get('Header 2', 'General Section')
        context_blocks += f"\n--- EXCERPT {i+1} (Source: {header}) ---\n"
        context_blocks += f"{item['document']}\n"

    system_instructions = (
        "You are an expert Genetics Assistant. Your goal is to answer questions using the provided textbook context. "
        "1. Be helpful and educational. "
        "2. If the answer is in the context, synthesize it clearly. "
        "3. If the context is related but doesn't have the exact answer, use the context as a 'hint' to provide a technically accurate response. "
    )

    user_message = f"""
    CONTEXT FROM TEXTBOOK:
    {context_blocks}

    USER QUESTION:
    {message}
    """

    response = client.models.generate_content(
        model=model,
        config=genai.types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=800,
            system_instruction=system_instructions,
        ),
        contents=user_message
    )

    return response.text



def wfwefwe():
    BASEDIR = Path(__file__).resolve().parent
    path_vector_db = os.path.join(BASEDIR, "../../vector_db")
    load_dotenv()
    # Example usage
    client = genai.Client()
    db_client = chromadb.PersistentClient(path=path_vector_db)
    # collection = db_client.get_or_create_collection(name="genetics_textbook")
    collection = db_client.get_collection(name="biology_paragraphs")

    # biochemistry example
    query = "What are the primary functions of DNA polymerase?"
    # genetics example
    # query = "What is the role of mRNA in protein synthesis?"
    # cell biology example
    # query = "Describe the structure and function of the mitochondrion."
    # physiology example
    # query = "Explain the process of muscle contraction."
    k = 5

    results = retrieve_docs(query, collection, client, k=k, threshold=0.8)

    for i in range(k):
        print(f"Document {i+1}:")
        print(f"Content: {results[i]['document']}")
        print(f"Distance: {results[i]['dist']:.4f}")
        print(f"Metadata: {results[i]['metadata']}")
        print()
        
    response = process_query(
        message=query,
        db_client=db_client,
        collection=collection,
        client=client,
        model="gemini-2.0-flash"
    )
    
    print(f"Final Response:\n{response}")
    
# wfwefwe()