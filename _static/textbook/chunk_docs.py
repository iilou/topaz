from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def chunk_textbook_docs(docs: list[Document], chunk_size: int = 1000, chunk_overlap: int = 200, debug_logs: list[str] | None = None) -> list[Document]:
    """
    Chunks the cleaned textbook documents into smaller pieces.
    Args:
        docs (list[Document]): List of cleaned textbook documents.
        chunk_size (int): The maximum size of each chunk.
        chunk_overlap (int): The number of overlapping characters between chunks.
    Returns:
        list[Document]: List of chunked textbook documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(docs)
    
    return chunks
    
    