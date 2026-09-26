import ollama

def ask(model: str, prompt: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]

    response = ollama.chat(model=model, messages=messages)
    return response["message"]["content"]
