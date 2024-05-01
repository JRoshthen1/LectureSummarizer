FROM python:3.10.12

WORKDIR /LectureSummarizer

COPY . /LectureSummarizer

RUN pip install --no-cache-dir \
    sounddevice \
    soundfile \
    numpy \
    openai-whisper \
    torch \
    scikit-learn \
    nltk \
    llama-cpp-python

CMD ["python", "main.py"]