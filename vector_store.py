# vector_store.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, dim=384):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add_texts(self, texts):
        embeddings = self.model.encode(texts)
        self.index.add(np.array(embeddings).astype("float32"))
        self.texts.extend(texts)

    def search(self, query, k=3):
        q_emb = self.model.encode([query]).astype("float32")
        D, I = self.index.search(q_emb, k)
        return [self.texts[i] for i in I[0]]
