# planner.py

def choose_tool(query: str) -> str:
    q = query.lower().strip()

    # SQL detection first
    if q.startswith("select") or " from " in q:
        return "sql"

    # Calculator detection
    if any(op in q for op in ["+", "-", "*", "/"]):
        return "calculator"

    return "rag"
