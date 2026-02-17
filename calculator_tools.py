# tools/calculator_tool.py
def calculator_tool(query: str) -> str:
    try:
        result = eval(query)
        return f"Calculator result: {result}"
    except:
        return "Calculator could not solve the expression."

