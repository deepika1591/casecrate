import chromadb.utils.embedding_functions as ef

embedder = ef.DefaultEmbeddingFunction()
vec = embedder(["they stopped my pension without hearing me"])[0]
print("dims:", len(vec))