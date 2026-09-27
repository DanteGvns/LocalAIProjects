import tkinter as tk
from tkinter import ttk, scrolledtext
from OfflineHandler import ask

class OfflineChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Offline AI Assistant (Ollama)")
        self.root.geometry("600x600")

        # --- Model Selection ---
        self.model_label = ttk.Label(root, text="Select Model:")
        self.model_label.pack(pady=5)

        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(
            root,
            textvariable=self.model_var,
            values=[
                "qwen2.5-coder:3b",
                "phi3",
                "qwen3:4b",
                "qwen3:8b"
            ],
            state="readonly"
        )
        self.model_dropdown.current(0)
        self.model_dropdown.pack(pady=5)

        # --- Chat Display ---
        self.chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=25)
        self.chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Formatting tags
        self.chat_box.tag_config("user_header", foreground="#1E90FF", font=("Segoe UI", 11, "bold"))
        self.chat_box.tag_config("assistant_header", foreground="#228B22", font=("Segoe UI", 11, "bold"))
        self.chat_box.tag_config("body", foreground="#000000", font=("Segoe UI", 11))
        self.chat_box.tag_config("indent", lmargin1=20, lmargin2=40)

        self._append_chat("assistant", "Ready.", model=None)

        # --- User Input ---
        self.entry = ttk.Entry(root, width=80)
        self.entry.pack(padx=10, pady=5)
        self.entry.bind("<Return>", self.send_message)

        # --- Send Button ---
        self.send_button = ttk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

    def send_message(self, event=None):
        user_text = self.entry.get().strip()
        if not user_text:
            return

        model = self.model_var.get()

        # Show user message FIRST
        self._append_chat("user", user_text)

        # Clear input box
        self.entry.delete(0, tk.END)

        # Now call the AI
        try:
            response = ask(model, user_text)
        except Exception as e:
            response = f"[Error] {e}"

        # Show assistant response
        self._append_chat("assistant", response, model)

    def _append_chat(self, role, text, model=None):
        self.chat_box.config(state=tk.NORMAL)

        if role == "user":
            self.chat_box.insert(tk.END, "\nUser:\n", "user_header")
            self.chat_box.insert(tk.END, text + "\n", ("body", "indent"))
        else:
            header = f"\nAssistant ({model}):\n" if model else "\nAssistant:\n"
            self.chat_box.insert(tk.END, header, "assistant_header")
            self.chat_box.insert(tk.END, text + "\n", ("body", "indent"))

        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = OfflineChatGUI(root)
    root.mainloop()
