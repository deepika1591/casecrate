mods = ["numpy", "onnxruntime", "tokenizers", "sklearn",
        "scipy", "chromadb", "grpc", "torch", "sentence_transformers"]

for m in mods:
    try:
        __import__(m)
        print("OK   ", m)
    except Exception as e:
        print("BLOCK", m, "->", type(e).__name__, str(e)[:60])