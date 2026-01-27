import re
from langchain_core.documents import Document
from utils import (
    is_termination_char,
    get_function_word_ratio,
    get_uppercase_ratio,
    get_proper_case_ratio,
    get_lower_case_ratio,
    get_punctuation_ratio,
)
import spacy

nlp = spacy.load("en_core_web_sm")

def clean_doc_function_GENETICS(docs: list[Document], debug_logs: list[str] | None = None) -> (list[Document]):
    def strip_pages(docs: list[Document], page_list: list[any], page_metadatas: list[any]) -> tuple[list[any], list[any]]:
        """
        trims noisy textbook pages of table header, image captions, noisy text, etc.
        """
        
        # --------------------------------------------------------------
        # Helper functions
        # --------------------------------------------------------------
        def get_page_number_and_desc(last_line: str) -> tuple[str, str] | None:
            page_number = None
            description = None
            
            pg_match1 = re.match(r"^(\d+)\s+(.+)$", last_line)
            pg_match2 = re.match(r"^(.+)\s+(\d+)$", last_line)
            
            if pg_match1:
                page_number = pg_match1.group(1)
            elif pg_match2:
                page_number = pg_match2.group(2)
                
            description = last_line.replace(page_number, "").strip() if page_number else None
            
            return (page_number, description) if page_number else None
             
        def is_line_figure_or_table(line: str) -> bool:
            line = line.lstrip()
            
            # patterns: Figure 1.2, Figure 3, Table 2.1, Table 4, ONLY at start of line
            figure_pattern = r"^(Figure|Fig\.?)\s*\d+(\.\d+)?"
            table_pattern = r"^Table\s*\d+(\.\d+)?"
            
            if re.match(figure_pattern, line) or re.match(table_pattern, line):
                return True
            return False
        
        def to_keep_long_line(line: str, line_info: dict) -> bool:
            return not(
                line_info["is_figure_or_table"] or
                line_info["uppercase_ratio"] > 0.5 or
                (line_info["func_word_ratio"] < 0.2 and line_info["lowercase_ratio"] < 0.4 and re.match(r".*\d$", line)) or
                (line_info["func_word_ratio"] < 0.12 and line_info["lowercase_ratio"] < 0.3)
            )
            
        def to_keep_short_line(line: str, line_info: dict) -> bool:
            return (
                line_info["is_termination_last_char"] and
                (line_info["uppercase_ratio"] < 0.5) and
                not line_info["is_figure_or_table"]
            )

        def add_paragraph(doc_metadata: dict, current_paragraph: list[str], paragraphs: list[any], paragraph_metadatas: list[dict], page_info: tuple[str, str] | None):
            if current_paragraph:
                paragraphs.append(current_paragraph)
                paragraph_metadatas.append({
                    "page_number": page_info[0] if page_info else "",
                    "page_description": page_info[1] if page_info else "",
                    "page": doc_metadata.get("page", ""),
                    "total_pages": doc_metadata.get("total_pages", ""),
                })
                
        def get_line_info(line: str) -> dict:
            function_word_ratio = 1.0
            try:
                get_function_word_ratio(line, nlp)
            except Exception as e:
                print(f"Error processing line for function word ratio: '{line}'. Error: {e}")
                
            return {
                "func_word_ratio": function_word_ratio,
                "uppercase_ratio": get_uppercase_ratio(line),
                "propercase_ratio": get_proper_case_ratio(line),
                "lowercase_ratio": get_lower_case_ratio(line),
                "is_figure_or_table": is_line_figure_or_table(line),
                "is_termination_last_char": is_termination_char(line[-1]),
            }
            
        # --------------------------------------------------------------
        # Main processing
        # --------------------------------------------------------------
        
        CHAR_THRESHOLD = 50
        
        for i, doc in enumerate(docs):
            lines = [line.strip() for line in doc.page_content.split("\n") if line.strip()]
            
            paragraphs = []
            paragraph_metadatas = []
            current_paragraph = []
            
            last_line = lines[-1] if lines else ""
            
            page_info = get_page_number_and_desc(last_line)
            
            for i, line in enumerate(lines[:-1]):  # exclude last line (page number/description)
                if len(line) == 0:
                    continue
                
                line_info = get_line_info(line)
                assert "is_figure_or_table" in line_info and "uppercase_ratio" in line_info and "func_word_ratio" in line_info and "lowercase_ratio" in line_info and "is_termination_last_char" in line_info
                
                # process short lines (end of paragraph)
                if (len(line) < CHAR_THRESHOLD):
                    # discard if start of paragraph is short (likely header or not useful)
                    if len(current_paragraph) == 0:
                        continue 
                    
                    if to_keep_short_line(line, line_info):
                        current_paragraph.append(line)
                    else:
                        if debug_logs is not None:
                            debug_logs.append(f"DISCARDED SHORT LINE: '{line}' info: {line_info}")
                    
                    add_paragraph(doc.metadata, current_paragraph, paragraphs, paragraph_metadatas, page_info)
                    current_paragraph = []
                    
                # process long lines (within paragraph)
                else:
                    if to_keep_long_line(line, line_info):
                        current_paragraph.append(line)
                    else:
                        if debug_logs is not None:
                            debug_logs.append(f"DISCARDED LONG LINE: '{line}' info: {line_info}")
                        
            # add any remaining paragraph
            add_paragraph(doc.metadata, current_paragraph, paragraphs, paragraph_metadatas, page_info)
                
            page_list.append(paragraphs)
            page_metadatas.append(paragraph_metadatas)
            
        return page_list, page_metadatas

    def combine_paragraphs(page_list: list[any], page_metadatas: list[any]) -> tuple[list[str], list[dict]]:
        def metadata_validate(meta: dict) -> bool:
            if meta.get("page_number", "") == "":
                return False
            if meta.get("page_description", "") == "" or meta.get("page_description", "").lower() in {"references", "bibliography", "index", "hints and solutions", "glossary", "", "problems"}:
                return False
            if meta.get("page", "") == "" or meta.get("total_pages", "") == "":
                return False
            return True
        
        def paragraph_validate(paragraph: list[str]):
            combined_text = "\n".join(paragraph)
            # if len(combined_text) < 150:
                # print("rejected due to length:", len(combined_text), "text:", combined_text)
                
                # return False
            punctuation_ratio = get_punctuation_ratio(combined_text)
            proper_case_ratio = get_proper_case_ratio(combined_text)
            
            if punctuation_ratio < 0.03 or proper_case_ratio > 0.3 or punctuation_ratio > 0.4:
                # print("rejected due to punctuation ratio:", punctuation_ratio, "text:", combined_text)
                if debug_logs is not None:
                    debug_logs.append(f"PARAGRAPH REJECTED DUE TO PUNCTUATION/PROPER CASE RATIO. Punctuation Ratio: {punctuation_ratio}, Proper Case Ratio: {proper_case_ratio}, Text: '{combined_text}'")
                return False
            return True
            
            
            
        
        paragraphs_combined = []
        paragraphs_combined_metadatas = []
        
        for i, page in enumerate(page_list):
            for j, paragraph in enumerate(page):
                if not metadata_validate(page_metadatas[i][j]) or not paragraph_validate(paragraph):
                    # print(f"rejected pg {page_metadatas[i][j].get('page_number', 'N/A')} desc: {page_metadatas[i][j].get('page_description', 'N/A')}")
                    if debug_logs is not None:
                        debug_logs.append(f"DISCARDED PARAGRAPH DURING COMBINE STEP. Metadata: {page_metadatas[i][j]}, Text: {' '.join(paragraph)}")
                    continue
                # print(f"accepted pg {page_metadatas[i][j].get('page_number', 'N/A')} desc: {page_metadatas[i][j].get('page_description', 'N/A')}")
                if debug_logs is not None:
                    debug_logs.append(f"ACCEPTED PARAGRAPH DURING COMBINE STEP. Metadata: {page_metadatas[i][j]}, Text: {' '.join(paragraph)}")
                
                if len(paragraphs_combined) == 0:
                    paragraphs_combined.append(paragraph)
                    paragraphs_combined_metadatas.append(page_metadatas[i][j])
                    continue
                
                # check if can combine with last paragraph
                last_paragraph = paragraphs_combined[-1]
                
                if not is_termination_char(last_paragraph[-1][-1]):
                    # combine
                    last_paragraph.extend(paragraph)
                else:
                    paragraphs_combined.append(paragraph)
                    paragraphs_combined_metadatas.append(page_metadatas[i][j])
                    
        return paragraphs_combined, paragraphs_combined_metadatas
                
            
    
    (page_list, page_metadatas) = strip_pages(docs, [], [])
    (paragraphs_combined, paragraphs_combined_metadatas) = combine_paragraphs(page_list, page_metadatas)
    
    # clean for paragraph length
    for i in range(len(paragraphs_combined)):
        combined_text = "\n".join(paragraphs_combined[i])
        if len(combined_text) < 200:
            if debug_logs is not None:
                debug_logs.append(f"POST COMBINE: DISCARDED PARAGRAPH DUE TO LENGTH < 200: '{combined_text}'")
            paragraphs_combined[i] = None
            paragraphs_combined_metadatas[i] = None
        print(f"para {i} : {paragraphs_combined[i]}")
        
    paragraphs_combined = [paragraphs_combined[i] for i in range(len(paragraphs_combined)) if paragraphs_combined[i] is not None]
    paragraphs_combined_metadatas = [paragraphs_combined_metadatas[i] for i in range(len(paragraphs_combined_metadatas)) if paragraphs_combined_metadatas[i] is not None]
    
    if len(paragraphs_combined) > 0:
        cleaned_docs = [
            Document(
                page_content="\n".join(paragraphs_combined[i]),
                metadata=paragraphs_combined_metadatas[i]
            )
            for i in range(len(paragraphs_combined))
        ]
        return cleaned_docs
    return []
