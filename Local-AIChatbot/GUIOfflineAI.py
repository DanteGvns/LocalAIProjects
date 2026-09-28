import tkinter as tk
import re
from queue import Empty, Queue
from threading import Thread
from tkinter import ttk

from OfflineHandler import ask


class OfflineChatGUI:
    BG = "#f3f5f7"
    SURFACE = "#ffffff"
    TEXT = "#17212b"
    MUTED = "#64717d"
    ACCENT = "#176b5b"
    ACCENT_ACTIVE = "#115347"
    BORDER = "#d9dee3"

    def __init__(self, root):
        self.root = root
        self.root.title("Local Assistant")
        self.root.geometry("780x770")
        self.root.minsize(560, 520)
        self.root.configure(bg=self.BG)

        self._responses = Queue()
        self._is_generating = False
        self.model_var = tk.StringVar(value="qwen2.5-coder:3b")
        self.status_var = tk.StringVar(value="Ready")

        self._configure_styles()
        self._build_header()
        self._build_chat()
        self._build_composer()

        self._append_chat("assistant", "Ready when you are.")
        self.entry.focus_set()
        self.root.after(100, self._poll_responses)

    def _configure_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("App.TFrame", background=self.BG)
        style.configure("Surface.TFrame", background=self.SURFACE)
        style.configure(
            "Title.TLabel",
            background=self.SURFACE,
            foreground=self.TEXT,
            font=("Segoe UI Semibold", 16),
        )
        style.configure(
            "Muted.TLabel",
            background=self.SURFACE,
            foreground=self.MUTED,
            font=("Segoe UI", 9),
        )
        style.configure(
            "Accent.TButton",
            background=self.ACCENT,
            foreground="#ffffff",
            borderwidth=0,
            padding=(18, 9),
            font=("Segoe UI Semibold", 10),
        )
        style.map(
            "Accent.TButton",
            background=[("active", self.ACCENT_ACTIVE), ("disabled", "#9ba7a4")],
        )
        style.configure(
            "Quiet.TButton",
            background=self.SURFACE,
            foreground=self.MUTED,
            bordercolor=self.BORDER,
            padding=(12, 7),
        )

    def _build_header(self):
        header = ttk.Frame(self.root, style="Surface.TFrame", padding=(22, 16))
        header.pack(fill=tk.X)
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text="Local Assistant", style="Title.TLabel").grid(
            row=0, column=0, sticky=tk.W
        )
        ttk.Label(
            header, textvariable=self.status_var, style="Muted.TLabel"
        ).grid(row=1, column=0, sticky=tk.W, pady=(2, 0))

        ttk.Label(header, text="MODEL", style="Muted.TLabel").grid(
            row=0, column=1, sticky=tk.W, padx=(18, 0)
        )
        self.model_dropdown = ttk.Combobox(
            header,
            textvariable=self.model_var,
            values=[
                "qwen2.5-coder:3b",
                "phi3",
                "qwen3:4b",
                "qwen3:8b"
            ],
            state="readonly",
            width=20,
        )
        self.model_dropdown.grid(row=1, column=1, sticky=tk.E, padx=(18, 0), pady=(3, 0))

        self.clear_button = ttk.Button(
            header, text="Clear", style="Quiet.TButton", command=self.clear_chat
        )
        self.clear_button.grid(row=0, column=2, rowspan=2, padx=(12, 0))

    def _build_chat(self):
        chat_frame = ttk.Frame(self.root, style="App.TFrame", padding=(22, 18, 22, 10))
        chat_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_box = tk.Text(
            chat_frame,
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=0,
            padx=22,
            pady=14,
            background=self.SURFACE,
            foreground=self.TEXT,
            font=("Segoe UI", 11),
            cursor="arrow",
            state=tk.DISABLED,
        )
        scrollbar = ttk.Scrollbar(chat_frame, command=self.chat_box.yview)
        self.chat_box.configure(yscrollcommand=scrollbar.set)
        self.chat_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_box.tag_configure(
            "user_header", foreground="#2563a6", font=("Segoe UI Semibold", 10), spacing1=12
        )
        self.chat_box.tag_configure(
            "assistant_header", foreground=self.ACCENT, font=("Segoe UI Semibold", 10), spacing1=12
        )
        self.chat_box.tag_configure(
            "body", foreground=self.TEXT, font=("Segoe UI", 11), spacing3=6
        )
        self.chat_box.tag_configure("error", foreground="#a33a32")
        self.chat_box.tag_configure(
            "markdown_h1",
            foreground=self.TEXT,
            font=("Segoe UI Semibold", 16),
            spacing1=12,
            spacing3=5,
        )
        self.chat_box.tag_configure(
            "markdown_h2",
            foreground=self.TEXT,
            font=("Segoe UI Semibold", 14),
            spacing1=10,
            spacing3=4,
        )
        self.chat_box.tag_configure(
            "markdown_h3",
            foreground=self.TEXT,
            font=("Segoe UI Semibold", 12),
            spacing1=8,
            spacing3=3,
        )
        self.chat_box.tag_configure(
            "bold", font=("Segoe UI Semibold", 11)
        )
        self.chat_box.tag_configure(
            "italic", font=("Segoe UI", 11, "italic")
        )
        self.chat_box.tag_configure(
            "inline_code",
            background="#edf1f3",
            foreground="#9b342c",
            font=("Cascadia Mono", 10),
        )
        self.chat_box.tag_configure(
            "code_label",
            background="#dfe5e8",
            foreground=self.MUTED,
            font=("Segoe UI Semibold", 8),
            lmargin1=14,
            lmargin2=14,
            spacing1=8,
        )
        self.chat_box.tag_configure(
            "code",
            background="#edf1f3",
            foreground="#26343d",
            font=("Cascadia Mono", 10),
            lmargin1=14,
            lmargin2=14,
            rmargin=14,
        )
        self.chat_box.tag_configure(
            "list", lmargin1=12, lmargin2=30, spacing1=2, spacing3=2
        )
        self.chat_box.tag_configure(
            "quote",
            foreground=self.MUTED,
            font=("Segoe UI", 11, "italic"),
            lmargin1=18,
            lmargin2=18,
            spacing1=4,
            spacing3=4,
        )
        self.chat_box.tag_configure(
            "rule", foreground=self.BORDER, spacing1=6, spacing3=6
        )

    def _build_composer(self):
        composer = ttk.Frame(self.root, style="Surface.TFrame", padding=(22, 14, 22, 18))
        composer.pack(fill=tk.X)
        composer.columnconfigure(0, weight=1)

        self.entry = tk.Text(
            composer,
            height=3,
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1,
            padx=12,
            pady=9,
            background="#fbfcfd",
            foreground=self.TEXT,
            insertbackground=self.TEXT,
            highlightthickness=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.ACCENT,
            font=("Segoe UI", 11),
        )
        self.entry.grid(row=0, column=0, sticky=tk.EW, padx=(0, 12))
        self.entry.bind("<Control-Return>", self.send_message)

        self.send_button = ttk.Button(
            composer, text="Send", style="Accent.TButton", command=self.send_message
        )
        self.send_button.grid(row=0, column=1, sticky=tk.NS)

        ttk.Label(
            composer,
            text="Ctrl+Enter to send",
            style="Muted.TLabel",
        ).grid(row=1, column=0, sticky=tk.W, pady=(7, 0))

    def send_message(self, event=None):
        if self._is_generating:
            return "break"

        user_text = self.entry.get("1.0", tk.END).strip()
        if not user_text:
            return "break"

        model = self.model_var.get()
        self._append_chat("user", user_text)
        self.entry.delete("1.0", tk.END)
        self._set_generating(True, model)

        Thread(
            target=self._request_response,
            args=(model, user_text),
            daemon=True,
        ).start()
        return "break"

    def _request_response(self, model, user_text):
        try:
            response = ask(model, user_text)
            self._responses.put((True, model, response))
        except Exception as error:
            self._responses.put((False, model, str(error)))

    def _poll_responses(self):
        try:
            succeeded, model, response = self._responses.get_nowait()
        except Empty:
            pass
        else:
            if succeeded:
                self._append_chat("assistant", response, model)
                self.status_var.set("Ready")
            else:
                self._append_chat("error", f"Could not get a response: {response}")
                self.status_var.set("Request failed")
            self._set_generating(False)

        self.root.after(100, self._poll_responses)

    def _set_generating(self, generating, model=None):
        self._is_generating = generating
        state = tk.DISABLED if generating else tk.NORMAL
        self.send_button.configure(state=state)
        self.model_dropdown.configure(state="disabled" if generating else "readonly")
        self.status_var.set(f"{model} is thinking..." if generating else self.status_var.get())
        if not generating:
            self.entry.focus_set()

    def clear_chat(self):
        self.chat_box.configure(state=tk.NORMAL)
        self.chat_box.delete("1.0", tk.END)
        self.chat_box.configure(state=tk.DISABLED)
        self._append_chat("assistant", "Conversation cleared. Ready when you are.")

    def _append_chat(self, role, text, model=None):
        self.chat_box.configure(state=tk.NORMAL)

        if role == "user":
            self.chat_box.insert(tk.END, "YOU\n", "user_header")
            self.chat_box.insert(tk.END, f"{text}\n", "body")
        elif role == "error":
            self.chat_box.insert(tk.END, "ERROR\n", "assistant_header")
            self.chat_box.insert(tk.END, f"{text}\n", ("body", "error"))
        else:
            header = f"ASSISTANT  ·  {model}\n" if model else "ASSISTANT\n"
            self.chat_box.insert(tk.END, header, "assistant_header")
            self._insert_markdown(text)
            self.chat_box.insert(tk.END, "\n", "body")

        self.chat_box.configure(state=tk.DISABLED)
        self.chat_box.see(tk.END)

    def _insert_markdown(self, text):
        in_code_block = False

        for line in text.splitlines():
            fence = re.match(r"^\s*```\s*([^`]*)$", line)
            if fence:
                if in_code_block:
                    self.chat_box.insert(tk.END, "\n", "body")
                    in_code_block = False
                else:
                    language = fence.group(1).strip().upper() or "CODE"
                    self.chat_box.insert(tk.END, f" {language}\n", "code_label")
                    in_code_block = True
                continue

            if in_code_block:
                self.chat_box.insert(tk.END, f" {line}\n", "code")
                continue

            heading = re.match(r"^(#{1,6})\s+(.+)$", line)
            if heading:
                level = min(len(heading.group(1)), 3)
                self._insert_inline(heading.group(2), (f"markdown_h{level}",))
                self.chat_box.insert(tk.END, "\n", f"markdown_h{level}")
                continue

            if re.match(r"^\s*([-*_])(?:\s*\1){2,}\s*$", line):
                self.chat_box.insert(tk.END, "-" * 48 + "\n", "rule")
                continue

            unordered = re.match(r"^\s*[-*+]\s+(.+)$", line)
            if unordered:
                self.chat_box.insert(tk.END, "  \u2022  ", "list")
                self._insert_inline(unordered.group(1), ("body", "list"))
                self.chat_box.insert(tk.END, "\n", "list")
                continue

            ordered = re.match(r"^\s*(\d+)[.)]\s+(.+)$", line)
            if ordered:
                self.chat_box.insert(tk.END, f"  {ordered.group(1)}.  ", "list")
                self._insert_inline(ordered.group(2), ("body", "list"))
                self.chat_box.insert(tk.END, "\n", "list")
                continue

            quote = re.match(r"^\s*>\s?(.*)$", line)
            if quote:
                self._insert_inline(f"|  {quote.group(1)}", ("quote",))
                self.chat_box.insert(tk.END, "\n", "quote")
                continue

            if line.strip():
                self._insert_inline(line, ("body",))
                self.chat_box.insert(tk.END, "\n", "body")
            else:
                self.chat_box.insert(tk.END, "\n", "body")

        if in_code_block:
            self.chat_box.insert(tk.END, "\n", "body")

    def _insert_inline(self, text, base_tags=()):
        token_pattern = re.compile(
            r"(`[^`\n]+`|\*\*.+?\*\*|__.+?__|(?<!\*)\*[^*\n]+\*|(?<!_)_[^_\n]+_)"
        )
        position = 0

        for match in token_pattern.finditer(text):
            self.chat_box.insert(tk.END, text[position:match.start()], base_tags)
            token = match.group(0)

            if token.startswith("`"):
                content, tag = token[1:-1], "inline_code"
            elif token.startswith(("**", "__")):
                content, tag = token[2:-2], "bold"
            else:
                content, tag = token[1:-1], "italic"

            self.chat_box.insert(tk.END, content, (*base_tags, tag))
            position = match.end()

        self.chat_box.insert(tk.END, text[position:], base_tags)


if __name__ == "__main__":
    root = tk.Tk()
    app = OfflineChatGUI(root)
    root.mainloop()
