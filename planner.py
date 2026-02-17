# agent/planner.py
def plan(query):
    query = query.lower()

    if "sql" in query or "revenue" in query:
        return ["sql"]

    if "calculate" in query or any(op in query for op in ["+", "-", "*", "/"]):
        return ["calculator"]

    if "document" in query or "explain" in query:
        return ["rag"]

    return ["rag"]



def choose_tool(query: str) -> str:
    query = query.lower()

    if any(word in query for word in ["calculate", "+", "-", "*", "/"]):
        return "calculator"

    if any(word in query for word in ["sql", "database", "table"]):
        return "sql"

    return "rag"
