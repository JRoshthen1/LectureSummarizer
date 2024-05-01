
from llama_cpp import Llama
import tkinter as tk
from tkinter import ttk
import threading
from tkinter import filedialog

class LlmPage(tk.Frame):
    def __init__(self, parent, app_data):
        super().__init__(parent)
        self.app = parent
        self.app_data = app_data
        tk.Label(self, text="Notes", font=self.app_data.heading_font).grid(row=0, column=0, sticky="ew", pady=2, padx=2)
        tk.Label(self, text="Press the button bellow to select your LLM and generate notes according to the previously defined keywods (tested on gpt4all-falcon-newbpe-q4_0.gguf) other model output object might not match the display function", font=self.app_data.paragraph_font, wraplength=800, justify="left").grid(row=1, column=0, sticky="ew", pady=2, padx=2)


        self.text_widget = tk.Text(self, font=self.app_data.paragraph_font, wrap="word")
        self.text_widget.grid(row=3, column=0, sticky="nsew", pady=6, padx=6)

        self.start_button = ttk.Button(self, text="Select LLM and generate notes", command=self.start_llama_thread)
        self.start_button.grid(row=4, column=0, pady=2, padx=2)

        self.save_button = tk.Button(self, text="Save Notes", command=self.save_notes)
    # LLM MODEL FILE SELECTOR
    def browse_file(self):
        llm_model_filename = filedialog.askopenfilename(initialdir="./", title="Select your LLM (GGUF format)", filetypes=(("LLM binary file", "*.gguf"), ("All files", "*.*")))
        if llm_model_filename:
            return llm_model_filename

    def start_llama_thread(self):
        if self.app_data.modified_keywords is None:
            self.text_widget.insert(tk.END, "Keywords have not been set.")
        else:
            self.text_widget.delete('1.0', tk.END)
            self.text_widget.insert(tk.END, "Generating, Please wait...")

            operation_thread = threading.Thread(target=self.run_llama_operation, args=(self.app_data.modified_keywords,self.app_data.highlights,))  # Pass data explicitly
            operation_thread.start()

    def run_llama_operation(self, llmTopics, highlights):
        try:
            
            llm = Llama(model_path=self.browse_file(), n_ctx=2048,)
            output = llm(
                prompt=f"Genereate comprehensive, informative and factual descriptions for the provided keywords '{llmTopics}'.", # Prompt
                max_tokens=0,
            )
            self.text_widget.after(0, self.update_text_widget, output['choices'][0])
            self.save_button.grid(row=5, column=0, pady=2, padx=2)

        except Exception as e:
            print(f"Error during Llama operation: {e}")
            self.text_widget.after(0, self.update_text_widget, "An error occurred, please try again.")

    def update_text_widget(self, content):
        if self.winfo_exists():
            self.text_widget.delete('1.0', tk.END)
            self.text_widget.insert(tk.END, content)

    def save_notes(self):
        text = self.text_widget.get("1.0", "end-1c")  # Get all text from the textarea
        filename = f"recordings/notes_{self.app_data.lecture_filename}.txt"
        with open(filename, "w") as file:
            file.write(text)

