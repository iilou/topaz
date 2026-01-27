import json
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def remove_chapter_numbers(text):
    # original: 24.2The Structure of DNA
    # desired: The Structure of DNA
    return re.sub(r"^\d+(\.\d+)*", "", text).strip()

def info_density(text):
    doc = nlp(text)
    entities = len(doc.ents)
    nouns = len([token for token in doc if token.pos_ in {"NOUN", "PROPN"}])
    words = len(doc)
    return (entities + nouns) / max(words, 1)

def is_junk_paragraph(text):
    t = text.lower().strip()

    if len(t) < 400:
        return 1

    junk_starts = [
        "decide if", "match the", "in the example",
        "see figure",  "click", "review", "exercise",
        "fill in", "multiple choice", "true or false", "short answer",
        "define the", "explain the", "what is", "which of", "select the",
        "summarize the", "describe the", "list the", "identify the",
        "discuss the", "outline the", "compare and contrast", "why is",
        "how does", "what are", "what causes", "what effects", "what role",
        "what function", "what process", "what structure", "what type", "what term",
        "what concept", "what principle", "what theory", "what law",
        "watch", "view", "read the", "refer to", "answer the",
        "complete the", "calculate the", "analyze the", "interpret the",
        "in the example", "in the diagram", "in the table", "in the figure",
        "see", "see also", "for more information", "additional resources",
        "decide", "match", "based", "click", "review", "exercise", "figure", "how"
    ]
    
    junk_keywords = [
        "quiz", "test", "exercise", 
        "interactive", "click", "website", "explore", "review", "data system",
        "video", "animation", "simulation", "lab", "activity", "worksheet",
    ]

    if any(t.startswith(j) for j in junk_starts):
        return 1
    
    if info_density(text) < 0.1:
        return 2
    
    # if any word in text matches junk keywords
    if any(j in t for j in junk_keywords):
        return 1

    if t.endswith("?"):
        return 3

    return 0

def chunk_paragraphs(paragraphs, min_words=200):
    chunks = []
    current = []
    count = 0

    for p in paragraphs:
        words = p.split()
        if not words:
            continue

        # if count >= min_words:
    #     chunks.append(" ".join(current))
    #     current = []
    #     count = 0

    #     current.append(p)
    #     count += len(words)

    # if count >= min_words:
    #     chunks.append(" ".join(current))

    return chunks


def re_chunk_jsonl(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = [json.loads(l) for l in f]

    # group by chapter + section
    groups = {}
    for x in lines:
        key = (x["chapter"], x["section"], x["subsection"])
        groups.setdefault(key, []).append(x)

    out = []

    for (chapter, section, subsection), items in groups.items():
        # paragraphs = [x["text"] for x in items if not is_junk_paragraph(x["text"])]
        chapter = remove_chapter_numbers(chapter)
        
        # chunks = paragraphs
        unfiltered_paragraphs = [x["text"] for x in items]

        for i, chunk in enumerate(unfiltered_paragraphs):
            flag = is_junk_paragraph(chunk)
            if flag != 0:
                continue
            
            out.append({
                "chapter": chapter,
                "section": section == "intro" and chapter or section,
                "subsection": subsection == "intro" and (section == "intro" and chapter or section) or subsection,
                "chunk_id": i,
                "text": chunk,
                "url": items[0]["url"],
                # "embedding_text": f"CHAPTER: {chapter}\n\nSECTION: {section}\n\nSUBSECTION: {subsection}\n\nCONTENT: {chunk}"
                "embedding_text": f"CHAPTER: {chapter}\n\nSECTION: {section == 'intro' and chapter or section}\n\nSUBSECTION: {subsection == 'intro' and (section == 'intro' and chapter or section) or subsection}\n\nCONTENT: {chunk}"
            })

    with open(output_path, "w", encoding="utf-8") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")

    print(f"Wrote {len(out)} semantic chunks")

jsonl_path = "biology_mvp.jsonl"
output_path = "biology_mvp_chunkedv2.jsonl"

re_chunk_jsonl(jsonl_path, output_path)