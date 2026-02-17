# ui/streamlit_app.py
import streamlit as st
import requests

st.title("🧠 Agentic QA System with Memory")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Ask a question")

if st.button("Submit"):
    res = requests.post("http://localhost:8000/query", json={"question": query})

    data = res.json()

    st.session_state.history.append((query, data))

for q, data in st.session_state.history:
    st.write("### 🧑 User:", q)
    st.write("🛠 Tool Used:", data["tool_used"])
    st.write("**Answer:**")
    st.code(data["answer"])
