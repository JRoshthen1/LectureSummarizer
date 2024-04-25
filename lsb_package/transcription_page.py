import tkinter as tk
from tkinter import ttk
import threading
import whisper
import torch
import gc
from .keywords_page import KeywordsPage


class TranscriptionPage(tk.Frame):
    def __init__(self, parent, app_data):
        super().__init__(parent)
        self.app = parent
        self.app_data = app_data
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.transcription_description = """Wait until your audio input gets processed.
> You can pass citations to your notes by highlighting piece of text with **text to cite**
> Press <Control-f> when focused in text-area, to find the next match from the current cursor position
> Pressing "Extract Keywords" will save the modified transcription"""


        tk.Label(self, text="Transcription", font=self.app_data.heading_font).grid(row=0, column=0, columnspan=2, pady=5, padx=5)

        self.audio_filename_label = tk.Label(self, text="No file", font=self.app_data.mono_font)
        self.audio_filename_label.grid(row=1, column=0, pady=4)

        tk.Label(self, text=self.transcription_description, font=self.app_data.paragraph_font, justify="left").grid(row=3, column=0, columnspan=2, padx=20)

        self.transcription_textarea = tk.Text(self, wrap="word", font=self.app_data.paragraph_font)
        self.transcription_textarea.grid(row=6, column=0, sticky="nsew", pady=6, padx=6)

        # Search box (initially not displayed)
        self.search_box = tk.Entry(self)
        self.search_tooltip = tk.Label(self, text="enter a string and press enter", font=("DejaVu Sans", 10), justify="left")
        self.search_box.bind("<Return>", self.search_text)

        self.transcription_textarea.bind('<Control-a>', select_all)
        self.transcription_textarea.bind('<Control-A>', select_all)

        # Bind Ctrl+F to display the search box
        self.transcription_textarea.bind('<Control-f>', self.display_search_box)
        self.transcription_textarea.bind('<Control-F>', self.display_search_box)

        transcription_scrollbar = tk.Scrollbar(self, command=self.transcription_textarea.yview)
        transcription_scrollbar.grid(row=6, column=1, sticky="ns")
        self.transcription_textarea.config(yscrollcommand=transcription_scrollbar.set)

        tk.Button(self, text="Extract Keywords", command=self.forward_to_keywords_page).grid(row=7, column=0, columnspan=2, pady=5)


    def display_search_box(self, event):
        # Display the search box above the text area
        self.search_box.grid(row=4, column=0, pady=(0, 6), padx=6, sticky="ew")
        self.search_box.focus_set()
        self.search_tooltip.grid(row=5, column=0, sticky="ew")
    def search_text(self, event):
        # Get the search query from the Entry widget
        query = self.search_box.get()
        if not query:
            return

        # Starting position for the search (insert cursor position)
        start_pos = self.transcription_textarea.index(tk.INSERT)
        # Search for the query in the text area
        pos = self.transcription_textarea.search(query, start_pos, tk.END)

        if pos:
            # If found, move cursor to the start of the found text and select the text
            end_pos = f"{pos}+{len(query)}c"  # Calculate end position of the selection
            self.transcription_textarea.tag_remove(tk.SEL, "1.0", tk.END)
            self.transcription_textarea.tag_add(tk.SEL, pos, end_pos)
            self.transcription_textarea.mark_set(tk.INSERT, pos)
            self.transcription_textarea.see(pos)

        # Hide the search box after search
        self.search_box.grid_remove()
        self.search_tooltip.grid_remove()



    def insert_into_textarea(self, transcription):
        """Insert transcription text into the Text widget."""
        def update_text():
            self.transcription_textarea.delete('1.0', tk.END)
            self.transcription_textarea.insert(tk.END, transcription)
        self.transcription_textarea.after(0, update_text)

    def start_transcription_process(self, audio_filepath):
        """Start transcription threading process."""
        self.audio_filename_label.config(text=f"Filename: {audio_filepath}")
        # Check if the lecture_filename was skipped
        if audio_filepath == "skipped":
            self.insert_into_textarea("")
            return
        else:
            self.insert_into_textarea("Transcribing, please wait...")
            threading.Thread(target=self.create_transcription, args=(audio_filepath,), daemon=True).start()
            gc.collect()  # Collect garbage to free up memory (doesn't seem to work)

            return

    def create_transcription(self, audio_filepath): 
        """Transcribe with Whisper."""
        try:
            hw_device = "cuda" if torch.cuda.is_available() else "cpu"
            whisper_model = whisper.load_model("small", device=hw_device)
            device_label = tk.Label(self, text="Loaded Whisper on: " + hw_device, font=self.app_data.mono_font)
            device_label.grid(row=2, column=0, pady=4)

            transcription_text = whisper_model.transcribe(audio_filepath)
            self.insert_into_textarea(transcription_text['text'])

            
            # Collect garbage to free up memory (doesn't seem to work)
            del whisper_model
            if (hw_device=='cuda'):
                torch.cuda.empty_cache()
            gc.collect()  


        except Exception as e:
            print(f"Error during transcription: {e}")
            self.insert_into_textarea("Failed to transcribe audio.")
    
    def forward_to_keywords_page(self):
        transcribed_text = self.transcription_textarea.get("1.0", tk.END)
        self.app.show_frame(KeywordsPage)
        self.app.frames[KeywordsPage].start_kw_extraction_process(transcribed_text)

def select_all(event):
    text_widget = event.widget
    text_widget.tag_add(tk.SEL, "1.0", tk.END)
    text_widget.mark_set(tk.INSERT, "1.0")
    text_widget.see(tk.INSERT)
    return 'break'