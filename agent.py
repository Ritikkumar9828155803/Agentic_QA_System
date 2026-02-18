#agent


from planner import choose_tool
from calculator_tools import calculator_tool
from Rag_tool import rag_tool
from Sql_tools import sql_tool
from memory import add_to_memory, get_memory

def run_agent(query: str):
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
