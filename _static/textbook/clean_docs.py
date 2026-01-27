from langchain_core.documents import Document

from cleaning_functions.genetics_1 import clean_doc_function_GENETICS
from cleaning_functions.biochemistry_1 import clean_doc_function_BIOCHEM


cleaning_presets = {
    "genetics_1": clean_doc_function_GENETICS,
    "biochemistry_1": clean_doc_function_BIOCHEM,
}

def clean_textbook_docs(docs: list[Document], preset_name: str, debug_logs: list[str] | None = None) -> list[Document]:
    if preset_name not in cleaning_presets:
        raise ValueError(f"Preset '{preset_name}' not found in cleaning_presets.")
    
    cleaning_function = cleaning_presets[preset_name]
    cleaned_docs = cleaning_function(docs, debug_logs)
    return cleaned_docs