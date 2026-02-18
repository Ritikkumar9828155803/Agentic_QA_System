# rag_tool.py


from vector_store import retrieve

def rag_tool(query: str) -> str:
    context = retrieve(query)
    context_text = " ".join(context)
    return f"Based on documents: {context_text}"

