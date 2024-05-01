import tkinter as tk
from tkinter import ttk
import webbrowser
from datetime import datetime
import sounddevice as sd
import soundfile as sf
import threading
import numpy as np
from .transcription_page import TranscriptionPage

class StartPage(tk.Frame):
    def __init__(self, parent, app_data):
        super().__init__(parent)
        self.app = parent
        self.app_data = app_data
        self.recording = False
        self.recording_data = []
        
        
        tk.Label(self, text="Lecture Summary Bot", font=self.app_data.heading_font).pack(pady=5)
        self.start_page_description = tk.Label(self, text="Start by recording your lecture using selected input device.", font=self.app_data.paragraph_font, wraplength=400, justify="left")
        self.start_page_description.pack(pady=5)

        # Fetch all devices and filter for those with input channels
        all_devices = sd.query_devices()
        input_devices = {all_devices[i]['name']: i for i in range(len(all_devices)) if all_devices[i]['max_input_channels'] > 0}

        self.device_var = tk.StringVar()
        device_names = list(input_devices.keys())
        self.device_menu = ttk.Combobox(self, values=device_names, textvariable=self.device_var)
        if device_names:  # Automatically select the default input device if available
            self.device_var.set("default")
        self.device_menu.pack(pady=10)

        ttk.Button(self, text="Start Recording", command=self.start_recording).pack(pady=5)
        ttk.Button(self, text="Stop Recording", command=self.stop_recording).pack(pady=5)
        ttk.Button(self, text="Skip Recording", command=self.skip_recording_page).pack(pady=5)
    
        # Recording indicator
        self.recording_indicator = tk.Label(self, text="Recording: OFF", fg="red")
        self.recording_indicator.pack(pady=5)


        def open_license_dialog():
            webbrowser.open("https://www.gnu.org/licenses/gpl.html")
        label_link_license = tk.Label(self, text="click here for details. https://www.gnu.org/licenses/gpl.html", fg="blue", cursor="hand2")
        label_link_license.pack(side="bottom")
        label_link_license.bind("<Button-1>", lambda event: open_license_dialog())
        label_license = tk.Label(self, text="Lecture Summarizer Copyright (C) 2024 Martin Jaros\nThis program comes with ABSOLUTELY NO WARRANTY;\nThis is free software, and you are welcome to redistribute it under certain conditions;")
        label_license.pack(side="bottom")




    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.update_recording_indicator(True)
            self.recording_data = []
            device_index = sd.query_devices().index(sd.query_devices(self.device_var.get()))
            threading.Thread(target=self.record_audio, args=(device_index,)).start()

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.update_recording_indicator(False)

    def record_audio(self, device_index):
        try:
            with sd.InputStream(device=device_index, samplerate=16000, channels=1, callback=self.audio_callback):
                while self.recording:
                    sd.sleep(1000)
        finally:
            self.save_recording()

    def audio_callback(self, indata, frames, time, status):
        self.recording_data.append(indata.copy())

    def save_recording(self):
        date_time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.app_data.lecture_filename = f"lecture_{date_time_str}"
        audio_filepath = f"recordings/recording_{self.app_data.lecture_filename}.wav"
        sf.write(audio_filepath, np.concatenate(self.recording_data, axis=0), 16000)
        
        self.app.frames[TranscriptionPage].start_transcription_process(audio_filepath)
        self.app.show_frame(TranscriptionPage)

    def skip_recording_page(self):
        self.app.frames[TranscriptionPage].start_transcription_process("skipped")
        self.app.show_frame(TranscriptionPage)


    def update_recording_indicator(self, is_recording):
        if is_recording:
            self.recording_indicator.config(text="Recording: ON", fg="green")
        else:
            self.recording_indicator.config(text="Recording: OFF", fg="red")
