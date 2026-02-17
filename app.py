from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Agentic QA API is running"}

@app.post("/query")
def query(req: QueryRequest):
    return run_agent(req.question)

