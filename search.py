from huggingface_hub import hf_hub_download
from tokenizers import Tokenizer
import onnxruntime as ort, numpy as np

REPO = "sentence-transformers/all-MiniLM-L6-v2"
tok = Tokenizer.from_file(hf_hub_download(REPO, "tokenizer.json"))
tok.enable_truncation(max_length=256)
tok.enable_padding()
sess = ort.InferenceSession(hf_hub_download(REPO, "onnx/model.onnx"))


def embed(texts, batch=64):
    out = []
    for i in range(0, len(texts), batch):
        enc = tok.encode_batch(texts[i:i + batch])
        ids = np.array([e.ids for e in enc], dtype=np.int64)
        mask = np.array([e.attention_mask for e in enc], dtype=np.int64)
        h = sess.run(None, {"input_ids": ids,
                            "attention_mask": mask,
                            "token_type_ids": np.zeros_like(ids)})[0]
        m = mask[:, :, None].astype(np.float32)
        v = (h * m).sum(1) / np.maximum(m.sum(1), 1e-9)   # mean-pool
        out.append(v / np.linalg.norm(v, axis=1, keepdims=True))
    return np.vstack(out)


import json, os
chunks = json.load(open("chunks.json", encoding="utf-8"))
texts = [c["text"] for c in chunks]

if os.path.exists("vectors.npy"):     # already done? load it
    V = np.load("vectors.npy")
else:
    V = embed(texts)                  # 1319 x 384, about 70s
    np.save("vectors.npy", V)


def search(question, k=5):
    qv = embed([question])[0]
    dist = 1.0 - V @ qv              # cosine distance
    order = np.argsort(dist)[:k]
    return [(float(dist[i]), chunks[i]) for i in order]


if __name__ == "__main__":        # only when YOU run this file
    for d, c in search("the department withheld my retiral dues"):
        print(round(d, 3), c["case_no"], c["text"][:90])