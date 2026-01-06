from google import genai
from google.genai import types
import chromadb
# from dotenv import load_dotenv

# load_dotenv()

def retrieve_docs(query: str, collection: chromadb.api.Collection, client: genai.Client, k: int = 5, threshold: float = 0.8):
    """Retrieve relevant documents from the ChromaDB based on the query."""
    print(f"Retrieving docs for query: {query}")
    
    query_result = client.models.embed_content(
        model="text-embedding-004",
        contents=query,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )

    query_vector = query_result.embeddings[0].values

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=k
    )

    print(f"retrieved docs with confidences: {results['distances'][0]}")

    # filter out low confidence results
    valid_results = []
    for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
        if dist < threshold:
            valid_results.append({"document": doc, "metadata": meta, "dist": dist})
        else:
            print(f"filtered out low confidence doc (dist = {dist:.4f}, threshold = {threshold})")

    return valid_results


def testasdffs():
    # Example usage
    client = genai.Client()
    db_client = chromadb.PersistentClient(path="./genetics_db")
    collection = db_client.get_or_create_collection(name="genetics_textbook")

    query = "What are the primary functions of DNA polymerase?"
    k = 5

    results = retrieve_docs(query, collection, client, k=k, threshold=0.8)

    for i in range(k):
        print(f"Document {i+1}:")
        print(f"Content: {results[i]['document']}")
        print(f"Distance: {results[i]['dist']:.4f}")
        print(f"Metadata: {results[i]['metadata']}")
        print()

testasdffs()