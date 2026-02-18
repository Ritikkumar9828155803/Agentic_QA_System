# vector_store.py


import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

documents = []
index = None

def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def build_index(text_chunks):
    global documents, index

    documents = text_chunks
    embeddings = model.encode(text_chunks)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

def load_text_file():
    try:
        with open("knowledge.txt", "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)
        build_index(chunks)
    except:
        pass

def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    chunks = chunk_text(text)
    build_index(chunks)

def retrieve(query, k=3):
    if index is None:
        return ["No documents loaded"]

    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)

    return [documents[i] for i in indices[0]]
