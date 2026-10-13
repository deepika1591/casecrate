import json
import random

chunks = json.load(
    open("chunks.json", encoding="utf-8")
)

for c in random.sample(chunks, 3):
    print(c["case_no"], "|", len(c["text"]), "chars")
    print(c["text"][:400], "\n---")