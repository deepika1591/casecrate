import re, json
from pathlib import Path

CHUNK_SIZE = 800        # characters, roughly a long paragraph
CHUNK_OVERLAP = 150     # carry the tail of the previous chunk

BODY = re.compile(r"(?m)^\s*ORAL (?:JUDGMENT|ORDER)")

def clean(text):
    text = re.sub(r"(?m)^\s*Patna High Court .*\n\s*\d+/\d+\s*$",
                  " ", text)                 # running header + page number
    text = re.sub(r"={5,}",   " ", text)    # the rule line
    text = re.sub(r"\.{3,}", " ", text)     # ...  ...  Appellant/s
    text = re.sub(r"\n{3,}",  "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    m = BODY.search(text)                  # drop the party block
    if m:
        text = text[m.start():]
    return text.strip()

META = {m["file"]: m for m in json.load(
    open("documents/documents.json", encoding="utf-8"))}

def read_metadata(path):
    m = META.get(path.name, {})
    return {"case_no": m.get("case_no", "?"),
            "court": m.get("court", "Patna High Court"),
            "date": m.get("decision_date", ""),
            "source_file": path.name}

def make_chunk(text, meta, chunk_index):
    return {"text": text.strip(), "chunk_index": chunk_index, **meta}

PARA = re.compile(r"\n(?=\s*\d{1,2}\.\s)")   # "\n2. " = a numbered paragraph

def split_paragraphs(text):
    paragraphs = []
    for block in PARA.split(text):
        block = " ".join(block.split())        # undo the PDF line breaks
        while len(block) > CHUNK_SIZE:         # huge paragraph? cut at a full stop
            cut = block.rfind(". ", 0, CHUNK_SIZE)
            if cut == -1:
                cut = CHUNK_SIZE
            paragraphs.append(block[:cut + 1].strip())
            block = block[cut + 1:]
        if block.strip():
            paragraphs.append(block.strip())
    return paragraphs

def chunk_document(text, meta):
    paragraphs = split_paragraphs(text)
    chunks, current = [], ""

    for para in paragraphs:
        if len(current) + len(para) > CHUNK_SIZE and current:
            chunks.append(make_chunk(current, meta, len(chunks)))
            current = current[-CHUNK_OVERLAP:].split(" ", 1)[-1]
        current += " " + para

    if current.strip():
        chunks.append(make_chunk(current, meta, len(chunks)))
    return chunks

all_chunks = []
for path in Path("documents").glob("*.txt"):
    meta = read_metadata(path)              # case no, court, date
    text = clean(path.read_text(encoding="utf-8"))
    all_chunks.extend(chunk_document(text, meta))

json.dump(all_chunks, open("chunks.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"{len(all_chunks)} chunks from {len(list(Path('documents').glob('*.txt')))} judgments")