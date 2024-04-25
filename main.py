import tkinter as tk
from tkinter import ttk
from lsb_package import StartPage, TranscriptionPage, KeywordsPage, LlmPage

class AppData:
    def __init__(self):
        self._lecture_filename = None
        self._modified_keywords = None

    @property
    def lecture_filename(self):
        return self._lecture_filename

    @lecture_filename.setter
    def lecture_filename(self, value):
        self._lecture_filename = value

    @property
    def modified_keywords(self):
        return self._modified_keywords

    @modified_keywords.setter
    def modified_keywords(self, value):
        self._modified_keywords = value
    
    heading_font = ("DejaVu Sans", 20, "bold")
    paragraph_font = ("DejaVu Sans", 12)
    serif_font = ("DejaVu Serif", 12)
    mono_font = ("Courier", 11)

# class AppData:
#     lecture_filename = None
#     modified_keywords = None


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lecture Summary Bot")
        
        self.data = AppData() 
        style = ttk.Style()
        style.theme_use('clam')
        self.frames = {}
        for F in (StartPage, TranscriptionPage, KeywordsPage, LlmPage):
            frame = F(self, self.data)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartPage)    
    
    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()

