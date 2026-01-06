from google import genai
import chromadb

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
        "4. Always cite the Source (Header) provided in the context."
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

