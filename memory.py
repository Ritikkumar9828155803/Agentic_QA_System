# memory/memory.py


chat_history = []

def add_to_memory(user_q: str, answer: str):
    chat_history.append({"question": user_q, "answer": answer})

def get_memory():
    return chat_history[-5:]

