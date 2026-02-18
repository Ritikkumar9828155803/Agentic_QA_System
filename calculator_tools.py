# calculator_tool.py



def calculator_tool(query: str) -> str:
    try:
        expression = query.replace("calculate", "").strip()
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Calculator error: {str(e)}"
