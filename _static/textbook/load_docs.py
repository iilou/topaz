from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

def convert_textbook_to_langchain_docs(textbook_path: str, debug_logs: list[str] | None = None) -> list[Document]:
    loader = PyPDFLoader(textbook_path, mode="page")
    docs = loader.load()
    return docs