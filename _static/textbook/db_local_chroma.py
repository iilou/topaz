
# import chromadb
        
# from google import genai
# from google.genai import types
# from dotenv import load_dotenv

# from langchain_core.documents import Document

# load_dotenv()
# client = genai.Client()

# def add_to_vector_database(chroma_db_path, collection_name, docs: list[Document]):
#     """
#     Adds a list of Document objects to a Chroma vector database collection.
#     Each document is embedded using the "text-embedding-004" model, and the resulting vector,
#     along with the document content and metadata, is stored in the specified collection.-
#     Args:
#         chroma_db_path (str): Path to the Chroma database directory.
#         collection_name (str): Name of the collection to add documents to.
#         docs (list[Document]): List of Document objects to be embedded and stored.
#     Raises:
#         Any exceptions raised by the ChromaDB client or embedding model will propagate.
#     """
    
    
#     db_client = chromadb.PersistentClient(path=chroma_db_path)
#     collection = db_client.get_or_create_collection(name=collection_name)
    
#     for i, doc in enumerate(docs):
#         result = client.models.embed_content(
#             model="text-embedding-004",
#             contents=doc.page_content,
#             config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
#         )
        
#         vector = result.embeddings[0].values
        
#         collection.add(
#             ids=[str(i)],
#             embeddings=[vector],
#             documents=[doc.page_content],
#             metadatas=[doc.metadata],
#         )