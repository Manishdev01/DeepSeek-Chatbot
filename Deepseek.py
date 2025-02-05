import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import requests
import json
import re

class OptimizedChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DeepSeek-R1:1.5b - ManishDev01")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Modern color scheme
        self.colors = {
            "bg": "#2D2D2D",
            "fg": "#E0E0E0",
            "user": "#64B5F6",
            "ai": "#81C784",
            "think": "#757575",
            "status_bg": "#373737",
            "input_bg": "#404040",
            "button_bg": "#4A4A4A"
        }
        
        self._setup_styles()
        self._create_layout()
        
        # State management
        self.is_generating = False
        self.think_pattern = re.compile(r'<think>(.*?)</think>', re.DOTALL)
        
        # API configuration
        self.api_url = "http://your-VPS-IP/api/generate"
        self.model = "deepseek-r1:1.5b"

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Base styles
        self.style.configure('.', 
            background=self.colors["bg"],
            foreground=self.colors["fg"],
            font=('Segoe UI', 12),
            relief='flat'
        )
        
        # Widget-specific styles
        self.style.configure('TEntry',
            fieldbackground=self.colors["input_bg"],
            borderwidth=2,
            insertcolor=self.colors["fg"]
        )
        self.style.configure('TButton',
            background=self.colors["button_bg"],
            padding=8,
            borderwidth=0
        )
        self.style.map('TButton',
            background=[('active', self.colors["button_bg"]), ('disabled', '#333333')],
            foreground=[('active', self.colors["fg"])]
        )

    def _create_layout(self):
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Chat display area
        self.chat_frame = ttk.Frame(self.root)
        self.chat_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            state='disabled',
            bg=self.colors["bg"],
            fg=self.colors["fg"],
            insertbackground=self.colors["fg"],
            padx=20,
            pady=20,
            font=('Segoe UI', 12),
            relief='flat'
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew")
        
        # Configure text tags
        self.chat_display.tag_config("user", 
            foreground=self.colors["user"],
            spacing3=10,
            font=('Segoe UI', 12, 'bold')
        )
        self.chat_display.tag_config("ai",
            foreground=self.colors["ai"],
            spacing3=10
        )
        self.chat_display.tag_config("think",
            foreground=self.colors["think"],
            font=('Segoe UI', 10, 'italic')
        )
        
        # Input area
        input_frame = ttk.Frame(self.root)
        input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        self.user_input = ttk.Entry(input_frame)
        self.user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=8)
        self.user_input.bind("<Return>", lambda e: self.send_message())
        
        self.send_btn = ttk.Button(input_frame, text="➤", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Status bar
        self.status_bar = ttk.Label(
            self.root,
            relief='flat',
            anchor=tk.W,
            background=self.colors["status_bg"],
            font=('Segoe UI', 10),
            padding=(10, 5)
        )
        self.status_bar.grid(row=2, column=0, sticky="ew")

    def _update_ui(self, action, *args):
        if action == "user_message":
            self._add_message(args[0], "user")
        elif action == "thinking":
            self._show_thinking_indicator()
        elif action == "final_response":
            self._display_final_response(args[0])
        elif action == "status":
            self.status_bar.config(text=args[0])

    def _add_message(self, message, sender):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{'You' if sender == 'user' else 'AI'}: {message}\n\n", sender)
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def _show_thinking_indicator(self):
        self.chat_display.config(state='normal')
        self.thinking_pos = self.chat_display.index(tk.INSERT)
        self.chat_display.insert(tk.END, "AI is processing...\n\n", "think")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def _display_final_response(self, response):
        self.chat_display.config(state='normal')
        self.chat_display.delete(self.thinking_pos, tk.END)
        
        # Split and format content
        parts = []
        last_pos = 0
        for match in self.think_pattern.finditer(response):
            start, end = match.span()
            parts.append(("ai", response[last_pos:start]))
            parts.append(("think", match.group(1)))
            last_pos = end
        parts.append(("ai", response[last_pos:]))
        
        # Insert formatted content
        self.chat_display.insert(tk.END, "AI: ", "ai")
        for tag, text in parts:
            self.chat_display.insert(tk.END, text, tag)
        self.chat_display.insert(tk.END, "\n\n")
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def send_message(self):
        if self.is_generating or not (message := self.user_input.get().strip()):
            return
        
        self.user_input.delete(0, tk.END)
        self._update_ui("user_message", message)
        self._update_ui("thinking")
        self._update_ui("status", "Generating response...")
        
        threading.Thread(target=self._process_response, args=(message,), daemon=True).start()

    def _process_response(self, prompt):
        self.is_generating = True
        buffer = []
        
        try:
            with requests.post(
                self.api_url,
                json={"model": self.model, "prompt": prompt},
                stream=True,
                timeout=30
            ) as response:
                response.raise_for_status()
                for chunk in response.iter_lines():
                    if chunk:
                        try:
                            data = json.loads(chunk.decode('utf-8'))
                            if content := data.get("response"):
                                buffer.append(content)
                        except (UnicodeDecodeError, json.JSONDecodeError):
                            continue

            final_response = "".join(buffer)
            self.root.after(0, self._update_ui, "final_response", final_response)
            
        except requests.exceptions.RequestException as e:
            self.root.after(0, self._update_ui, "status", f"Error: {str(e)}")
        finally:
            self.root.after(0, lambda: self._update_ui("status", "Ready"))
            self.is_generating = False

if __name__ == "__main__":
    root = tk.Tk()
    app = OptimizedChatApp(root)
    root.mainloop()