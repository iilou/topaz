import os
import requests

BASE_URL = "https://api.fireworks.ai/inference/v1/rerank"

def rerank_results(query: str, docs: list[str], model: str = "accounts/fireworks/models/qwen3-reranker-8b") -> list[str]:
    """Rerank the retrieved documents based on their relevance to the query using Fireworks API."""

    API_KEY = os.environ["FIREWORKS_API_KEY"]
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": query,
        "documents": docs,
        "top_n": len(docs),
        "return_documents": True,
        "model": model
    }
    
    response = requests.post(BASE_URL, json=payload, headers=headers)
    response.raise_for_status()

    data = response.json()
    return data


# def testasdifjweiofjwef():
#     query = "What's the prim"