import time
from search import embed, search, V, chunks

print("chunks     :", len(chunks))
print("vectors    :", V.shape)
print("dims check :", embed(["hello"]).shape)

t0 = time.time()
embed([c["text"] for c in chunks[:200]])
secs = (time.time() - t0) * len(chunks) / 200
print("embed speed:", round(secs), "seconds for all 1319")

print("")
questions = ["the department withheld my retiral dues",
             "they stopped my pension without hearing me",
             "my appointment was cancelled after I had joined",
             "can I claim a flight delay refund in Singapore?",
             "how do I register a trademark in Japan?",
             "what is the recipe for chocolate cake?"]

for q in questions:
    print(round(search(q)[0][0], 3), q)