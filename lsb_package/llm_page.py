
from llama_cpp import Llama
import tkinter as tk
from tkinter import ttk
import threading

class LlmPage(tk.Frame):
    def __init__(self, parent, app_data):
        super().__init__(parent)
        self.app = parent
        self.app_data = app_data
        tk.Label(self, text="Notes", font=self.app_data.heading_font).grid(row=0, column=0, sticky="ew", pady=2, padx=2)
        tk.Label(self, text="Press the generate button and wait for your notes to generate.", font=self.app_data.paragraph_font, wraplength=400, justify="left").grid(row=1, column=0, sticky="ew", pady=2, padx=2)
        self.text_widget = tk.Text(self, font=self.app_data.paragraph_font, wrap="word")
        self.text_widget.grid(row=2, column=0, sticky="nsew", pady=6, padx=6)

        self.start_button = ttk.Button(self, text="Start Operation", command=self.start_llama_operation)
        self.start_button.grid(row=3, column=0, sticky="ew", pady=2, padx=2)

    def start_llama_operation(self):
        if self.app_data.modified_keywords is None:
            self.text_widget.insert(tk.END, "Keywords have not been set.")
        else:
            self.text_widget.delete('1.0', tk.END)
            self.text_widget.insert(tk.END, "Please wait...")

            operation_thread = threading.Thread(target=self.run_llama_operation, args=(self.app_data.modified_keywords,))  # Pass data explicitly
            operation_thread.start()

    def run_llama_operation(self, llmTopics):
        try:
            # Example: Llama class must be imported correctly here
            llm = Llama(model_path="##############", n_ctx=2048, )
            # output = llm.create_chat_completion(
            #     messages=[
            #         {"role": "system", "content": "You are a teacher explaining in great detail given topics divided by new line."},
            #         {"role": "user", "content": llmTopics}  # Use local variable passed to thread
            #     ]
            # )
            output = llm(
                f"Genereate comprehensive, informative and factual descriptions for the provided keywords '{llmTopics}", # Prompt
                max_tokens=0, # Generate up to 32 tokens, set to None to generate up to the end of the context window

            )
            """Generate text from a prompt.
            Args:
                prompt: The prompt to generate text from.
                suffix: A suffix to append to the generated text. If None, no suffix is appended.
                max_tokens: The maximum number of tokens to generate. If max_tokens <= 0 or None, the maximum number of tokens to generate is unlimited and depends on n_ctx.
                temperature: The temperature to use for sampling.
                top_p: The top-p value to use for nucleus sampling. Nucleus sampling described in academic paper "The Curious Case of Neural Text Degeneration" https://arxiv.org/abs/1904.09751
                min_p: The min-p value to use for minimum p sampling. Minimum P sampling as described in https://github.com/ggerganov/llama.cpp/pull/3841
                typical_p: The typical-p value to use for sampling. Locally Typical Sampling implementation described in the paper https://arxiv.org/abs/2202.00666.
                logprobs: The number of logprobs to return. If None, no logprobs are returned.
                echo: Whether to echo the prompt.
                stop: A list of strings to stop generation when encountered.
                frequency_penalty: The penalty to apply to tokens based on their frequency in the prompt.
                presence_penalty: The penalty to apply to tokens based on their presence in the prompt.
                repeat_penalty: The penalty to apply to repeated tokens.
                top_k: The top-k value to use for sampling. Top-K sampling described in academic paper "The Curious Case of Neural Text Degeneration" https://arxiv.org/abs/1904.09751
                stream: Whether to stream the results.
                seed: The seed to use for sampling.
                tfs_z: The tail-free sampling parameter. Tail Free Sampling described in https://www.trentonbricken.com/Tail-Free-Sampling/.
                mirostat_mode: The mirostat sampling mode.
                mirostat_tau: The target cross-entropy (or surprise) value you want to achieve for the generated text. A higher value corresponds to more surprising or less predictable text, while a lower value corresponds to less surprising or more predictable text.
                mirostat_eta: The learning rate used to update `mu` based on the error between the target and observed surprisal of the sampled word. A larger learning rate will cause `mu` to be updated more quickly, while a smaller learning rate will result in slower updates.
                model: The name to use for the model in the completion object.
                stopping_criteria: A list of stopping criteria to use.
                logits_processor: A list of logits processors to use.
                grammar: A grammar to use for constrained sampling.
                logit_bias: A logit bias to use.

            Raises:
                ValueError: If the requested tokens exceed the context window.
                RuntimeError: If the prompt fails to tokenize or the model fails to evaluate the prompt.

            Returns:
                Response object containing the generated text.
            """
            self.text_widget.after(0, self.update_text_widget, output['choices'][0])
        except Exception as e:
            print(f"Error during Llama operation: {e}")
            self.text_widget.after(0, self.update_text_widget, "An error occurred, please try again.")

    def update_text_widget(self, content):
        if self.winfo_exists():
            self.text_widget.delete('1.0', tk.END)
            self.text_widget.insert(tk.END, content)
