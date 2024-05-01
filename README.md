# Lecture Summarizer

## Description
Tkinter application to record text with openai-whisper, extract keywords from transcription with sklearn's TF-IDF and generate notes with gguf llm model 

## Requirements
Python 3.10.12
pip 24.0

## Installation

### Running Locally

Clone the repository:

```bash
git clone https://github.com/JRoshthen1/LectureSummarizer.git
```

Navigate to the project directory:

```bash
cd LectureSummarizer/
```

Install dependencies:

```bash
pip install tkinter sounddevice soundfile numpy openai-whisper torch scikit-learn nltk llama-cpp-python
```

## Usage

1. Create `recordings` directory in the root of the application (./recordings/)

2. Download a gguf model for text generation, [examples](https://huggingface.co/models?library=gguf)

3. Run the app
```bash
python3 main.py
```

## Contributing

- Start by forking the repository.
- Create a branch in your fork for your contributions.
- Commit your changes with clear commit messages.
- Push your branch to your fork on GitHub and submit a pull request to the main project.

## License

Lecture Summary Bot
Copyright (C) 2024  Martin Jaros

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

