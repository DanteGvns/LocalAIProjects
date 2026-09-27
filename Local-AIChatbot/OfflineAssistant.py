from OllamaClient import ask

def offline_assistant():
    """Simple offline AI chat bot using Ollama's Qwen model"""
    print("Starting offline assistant...")
    
    while True:
        try:
            prompt = input("User: ")
            response = ask("qwen2.5-coder:3b", prompt)
            print(f"\nAssistant: {response}")
        except KeyboardInterrupt:
            print("\nShutting down offline assistant...")
            break

if __name__ == "__main__":
    offline_assistant()