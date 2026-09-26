import ollama

#define the data and model

model = "phi3"

message = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What toppics go on a cheese pizza?"},
]

#create the chat and get response back

response = ollama.chat(model=model,messages=message)

print(response["message"]["content"])

