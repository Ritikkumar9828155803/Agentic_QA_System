# streamlit_app.py


import streamlit as st
import requests

st.title("Agentic QA System with Memory")

# 🔼 Upload CSV or PDF
uploaded_file = st.file_uploader("Upload CSV or PDF", type=["csv", "pdf"])

if uploaded_file is not None:
    files = {
        "file": (
            uploaded_file.name,          # ✅ send filename
            uploaded_file.getvalue(),    # ✅ send bytes
            uploaded_file.type           # ✅ send MIME type
        )
    }

    res = requests.post("http://localhost:8000/upload_file", files=files)

    if res.status_code == 200:
        response_json = res.json()

        if "message" in response_json:
            st.success(response_json["message"])
        elif "error" in response_json:
            st.error(response_json["error"])
        else:
            st.write(response_json)
    else:
        st.error("Upload failed")



# 💬 Query box
query = st.text_input("Ask a question")

if st.button("Submit") and query:
    try:
        res = requests.post(
            "http://localhost:8000/query",
            json={"question": query}
        )

        if res.status_code == 200:
            data = res.json()

            st.subheader("Answer")
            st.write(data["answer"])

            st.subheader("Tool Used")
            st.write(data["tool_used"])

            st.subheader("Memory")
            for item in data["memory"]:
                st.write(f"🧑 {item['question']}")
                st.write(f"🤖 {item['answer']}")
                st.write("---")

        else:
            st.error("API Error")

    except:
        st.error("FastAPI server is not running")
