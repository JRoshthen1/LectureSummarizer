import tkinter as tk
from tkinter import ttk
from nltk.stem import WordNetLemmatizer
from datetime import datetime
import re
#from sklearn.decomposition import NMF, LatentDirichletAllocation, MiniBatchNMF
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.tokenize import word_tokenize
from .llm_page import LlmPage


class KeywordsPage(tk.Frame):
    def __init__(self, parent, app_data):
        super().__init__(parent)
        self.app = parent
        self.app_data = app_data
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.keywords_description = 'Here are the extracted keywords. You can modify them to your liking before feeding them into note generation. Keywords will be added to the top of the transcription file.'

        
        tk.Label(self, text="Keywords", font=self.app_data.heading_font).grid(row=0, column=0, columnspan=2)
        
        self.lecture_filename_label = tk.Label(self, font=self.app_data.mono_font)
        self.lecture_filename_label.grid(row=1, column=0, pady=4)
        
        tk.Label(self, text=self.keywords_description, font=self.app_data.paragraph_font, wraplength=400, justify="left").grid(row=2, column=0, columnspan=2, pady=5, padx=5)

        self.keywords_textarea = tk.Text(self, wrap="word", font=self.app_data.paragraph_font)
        self.keywords_textarea.grid(row=3, column=0, sticky="nsew", pady=6, padx=6)

        keywords_scrollbar = tk.Scrollbar(self, command=self.keywords_textarea.yview)
        keywords_scrollbar.grid(row=3, column=1, sticky="ns")
        self.keywords_textarea.config(yscrollcommand=keywords_scrollbar.set)

        tk.Button(self, text="Generate Notes", command=self.write_kw_and_forward_to_llm_page).grid(row=4, column=0, columnspan=2, pady=5)


    def write_kw_and_forward_to_llm_page(self):
        self.modified_keywords = self.keywords_textarea.get('1.0', tk.END)
        self.app_data.modified_keywords = self.modified_keywords
        #print(self.app_data.modified_keywords)
        keywords = f"Transcription keywords:\n\n{self.modified_keywords}\n"
        filename = f"recordings/transcript_{self.app_data.lecture_filename}.txt"
        with open(filename, 'r') as file:
            transcription = file.read()
        with open(filename, 'w') as file:
            file.write(keywords)
            file.write(transcription)
        self.app.show_frame(LlmPage)


    def start_kw_extraction_process(self, transcription_text):
        # Save the transcription to a text file
        if (self.app_data.lecture_filename == None):
            date_time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.app_data.lecture_filename = f"lecture_{date_time_str}"
            filename = f"recordings/transcript_{self.app_data.lecture_filename}.txt"
            self.lecture_filename_label.config(text=filename)
        else:
            filename = f"recordings/transcript_{self.app_data.lecture_filename}.txt"
            self.lecture_filename_label.config(text=filename)
        
        with open(filename, "w") as file:
            file.write(transcription_text)

        # Extract the keywords
        keywords = self.extract_topics(transcription_text)
        self.keywords_textarea.delete('1.0', tk.END)
        self.keywords_textarea.insert(tk.END, "\n".join(keywords))

    def extract_topics(self, transcript):
        """Lemmatizing words into their simplest form"""
        lemmatizer = WordNetLemmatizer()

        # Split transcript into sentences
        sentences = re.split(r'[.!?]', transcript)

        # Initialize list to store lemmatized data
        cleaned_data = []

        # Preprocess and lemmatize each sentence
        for sentence in sentences:
            # Preprocess the sentence
            sentence = sentence.lower()
            sentence = re.sub(r'[^\w\s]', '', sentence)
            # Tokenize the preprocessed sentence
            words = word_tokenize(sentence)    
            # Lemmatize each word and join back to form the sentence
            lemmatized_sentence = ' '.join([lemmatizer.lemmatize(word, pos='v') for word in words])
            cleaned_data.append(lemmatized_sentence)


        """Setting tf-idf and NMF variables"""
        n_samples = len(cleaned_data)
        n_features = 20
        n_components = 10
        n_top_words = 10
        batch_size = 128
        init = "nndsvda"


        """Use tf-idf features for NMF"""
        data_samples = cleaned_data[:n_samples]
        tfidf_vectorizer = TfidfVectorizer(
            max_df=0.30,
            min_df=2,
            max_features=n_features,
            stop_words="english"
        )
        
        tfidf = tfidf_vectorizer.fit_transform(data_samples)
        
        tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
        
        #print("TF-IDF Feature names: ", tfidf_feature_names)


#        nmf = NMF(
#            n_components=n_components,
#            max_iter=n_samples,
#            #tol=1e-4,
#            random_state=1,
#            init=init,
#            beta_loss="frobenius",
#            alpha_W=0.00005, #directory theres run command dash, file way root theres echo, hello echo example say run, just run say things dash, know things command say theres, like things example theres way, program run echo way say, shell run things way command, use way things dash command, want root say example command
#            alpha_H=0.00005,
#            #alpha_W=0, # directory theres run command dash, file way root theres echo, hello echo example say run, just run say things dash, know things command say theres, like things example theres way, program run echo way say, shell run things way command, use way things dash command, want root say example command
#            #alpha_H=0,
#            l1_ratio=1,
#        ).fit(tfidf)

        topics_list = []

        # Collect the top words for each topic
        #for topic_idx, topic in enumerate(nmf.components_):
            # Get the top 5 words for this topic
        #    top_words = [tfidf_feature_names[i] for i in topic.argsort()[:-5 - 1:-1]]
            # Convert the list of top words to a string and add to the topics list
        #    topics_list.append(" ".join(top_words))

        topics = set(topics_list)  # Naive splitting by spaces
        #return sorted(topics)  # Return a sorted list of unique words
        return sorted(tfidf_feature_names)  # Return a sorted list of unique words

