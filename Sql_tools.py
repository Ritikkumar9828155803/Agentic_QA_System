# tools/sql_tool.py





import sqlite3

def sql_tool(query: str) -> str:
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        cursor.execute(query)
        rows = cursor.fetchall()

        conn.close()

        return str(rows)

    except Exception as e:
        return f"SQL Error: {str(e)}"
