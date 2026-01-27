import re
import spacy

def is_termination_char(char: str) -> bool:
    termination_chars = {".", "!", "?"}
    return char in termination_chars

def get_punctuation_ratio(line: str) -> float:
    if len(line) == 0:
        return 0.0
    punc = '''!.,?'''
    punctuation_chars = [c for c in line if c in punc]
    alpha_words = [w for w in line.split() if any(c.isalpha() for c in w)]
    ratio = len(punctuation_chars) / max(1, len(alpha_words))
    return ratio

def get_function_word_ratio(line: str, nlp: spacy.language.Language) -> float:
    token = nlp(line)
    function_tokens = [
        t for t in token
        if t.is_stop
    ]
    content_tokens = [
        t for t in token
        if t.pos_ not in {"PUNCT", "SPACE"} 
    ]
    
    return len(function_tokens) / max(1, len(content_tokens))

def get_uppercase_ratio(line: str) -> float:
    if len(line) == 0:
        return 0.0
    words = line.split()
    
    alpha_words = [w for w in words if any(c.isalpha() for c in w)]
    uppercase_words = [
        w for w in alpha_words
        if all(not c.islower() for c in w)
    ]

    ratio = len(uppercase_words) / max(1, len(alpha_words))
    return ratio

def get_proper_case_ratio(line: str) -> float:
    if len(line) == 0:
        return 0.0
    words = line.split()
    
    alpha_words = [w for w in words if any(c.isalpha() for c in w)]
    proper_case_words = [
        w for w in alpha_words
        if w[0].isupper() and all(not c.isupper() for c in w[1:])
    ]

    ratio = len(proper_case_words) / max(1, len(alpha_words))
    return ratio

def get_lower_case_ratio(line: str) -> float:
    if len(line) == 0:
        return 0.0
    words = line.split()
    
    alpha_words = [w for w in words if any(c.isalpha() for c in w)]
    lower_case_words = [
        w for w in alpha_words
        if all(not c.isupper() for c in w)
    ]
    ratio = len(lower_case_words) / max(1, len(alpha_words))
    return ratio

def is_text_question(line: str) -> bool:
    """
    condition 1: ends with ?
    condition 2: starts with common question words
    question_words = {"who", "what", "when", "where", "why", "how", "is", "are", "do", "does", "did", "can", "could", "would", "should"}
    condition 3: starts with "(number < 100 or single letter). (question_text)"
    """
    
    if len(line) == 0:
        return False
    
    question_words = {"who", "what", "when", "where", "why", "how", "is", "are", "do", "does", "did", "can", "could", "would", "should", "identify", "list", "name", "describe", "explain"}
    line_lower = line.lower().strip()
    # if line_lower.endswith("?"):
    #     return True
    first_word = line_lower.split()[0]
    if first_word in question_words:
        return True
    
    question_regex = r"^([A-Za-z]|\d{1,2})\.\s+.*"
    if re.match(question_regex, line_lower):
        return True
    
    return False