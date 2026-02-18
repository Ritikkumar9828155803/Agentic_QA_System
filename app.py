#app

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
import sqlite3
import shutil
import os

from agent import run_agent
from vector_store import load_pdf, load_text_file

app = FastAPI()

# 🔁 Load default text knowledge at startup
load_text_file()

# 📦 Request schema
class QueryRequest(BaseModel):
    question: str

# 🏠 Health check
@app.get("/")
def home():
    return {"message": "Agentic QA API is running"}

# 🔼 Unified upload endpoint (CSV + PDF)
@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    try:
        filename = file.filename.lower().strip()
        ext = os.path.splitext(filename)[1]

        # 📄 CSV → SQLite
        if ext == ".csv":
            df = pd.read_csv(file.file, encoding="utf-8", engine="python")

            conn = sqlite3.connect("data.db")
            df.to_sql("data", conn, if_exists="replace", index=False)
            conn.close()

            return {"message": "CSV uploaded → stored in SQLite as table 'data'"}

        # 📄 PDF → RAG
        elif ext == ".pdf":
            temp_path = f"temp_{filename}"

            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            load_pdf(temp_path)
            os.remove(temp_path)

            return {"message": "PDF uploaded → indexed for RAG"}

        # ❌ Unsupported file
        else:
            return {"error": f"Unsupported file type: {ext}"}

    except Exception as e:
        return {"error": f"Upload failed: {str(e)}"}

# 💬 Query endpoint (Agent)
@app.post("/query")
def query(req: QueryRequest):
    try:
        return run_agent(req.question)
    except Exception as e:
        return {"error": f"Agent error: {str(e)}"}
