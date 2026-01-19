import json

def is_junk_paragraph(text):
    t = text.lower().strip()

    if len(t) < 40:
        return True

    junk_starts = [
        "decide if", "match the", "based on", "in the example",
        "see figure", "figure", "table", "click", "review", "exercise"
    ]

    if any(t.startswith(j) for j in junk_starts):
        return True

    if t.endswith("?"):
        return True

    return False

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
        paragraphs = [x["text"] for x in items if not is_junk_paragraph(x["text"])]
        
        chunks = paragraphs

        for i, chunk in enumerate(chunks):
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
output_path = "biology_mvp_chunked.jsonl"

re_chunk_jsonl(jsonl_path, output_path)