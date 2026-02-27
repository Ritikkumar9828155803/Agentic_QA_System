import streamlit as st
import sqlite3
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

# -----------------------------
# GLOBAL MEMORY
# -----------------------------
chat_history = []

def add_to_memory(q, a):
    chat_history.append({"question": q, "answer": a})

def get_memory():
    return chat_history[-5:]

# -----------------------------
# EMBEDDING MODEL + VECTOR DB
# -----------------------------
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

def load_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    chunks = chunk_text(text)
    build_index(chunks)

def retrieve(query, k=3):
    global index
    if index is None:
        return ["No documents loaded"]

    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)
    return [documents[i] for i in indices[0]]

# -----------------------------
# TOOLS
# -----------------------------
def calculator_tool(query):
    try:
        expression = query.replace("calculate", "").strip()
        return str(eval(expression))
    except Exception as e:
        return f"Calculator error: {e}"

def sql_tool(query):
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return str(rows)
    except Exception as e:
        return f"SQL error: {e}"

def rag_tool(query):
    context = retrieve(query)
    return "Based on documents: " + " ".join(context)

# -----------------------------
# PLANNER
# -----------------------------
def choose_tool(query):
    q = query.lower().strip()

    if q.startswith("select") or " from " in q:
        return "sql"

    if any(op in q for op in ["+", "-", "*", "/"]):
        return "calculator"

    return "rag"

# -----------------------------
# AGENT
# -----------------------------
def run_agent(query):
    tool = choose_tool(query)

    if tool == "calculator":
        result = calculator_tool(query)

    elif tool == "sql":
        result = sql_tool(query)

    else:
        result = rag_tool(query)

    add_to_memory(query, result)

    return {
        "tool_used": tool,
        "answer": result,
        "memory": get_memory()
    }

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("🧠 Agentic QA System (Cloud Version)")

st.write("Upload a PDF (for RAG) or CSV (for SQL queries)")

uploaded_file = st.file_uploader("Upload CSV or PDF", type=["csv", "pdf"])

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        conn = sqlite3.connect("data.db")
        df.to_sql("data", conn, if_exists="replace", index=False)
        conn.close()
        st.success("CSV uploaded and stored in SQLite as table 'data'")

    elif uploaded_file.name.endswith(".pdf"):
        load_pdf(uploaded_file)
        st.success("PDF indexed for RAG")

# Query Section
query = st.text_input("Ask a question")

if st.button("Submit") and query:
    result = run_agent(query)

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Tool Used")
    st.write(result["tool_used"])

    st.subheader("Recent Memory")
    for item in result["memory"]:
        st.write(f"🧑 {item['question']}")
        st.write(f"🤖 {item['answer']}")
        st.write("---")