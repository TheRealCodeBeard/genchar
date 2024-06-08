from huggingface_hub import hf_hub_download
from llama_cpp import Llama
import re

class Brain():
    @classmethod
    def get_base_brain(cls):
        model_name = "microsoft/Phi-3-mini-4k-instruct-gguf"##"TheBloke/Mistral-7B-OpenOrca-GGUF"
        model_file = "Phi-3-mini-4k-instruct-q4.gguf" ##"mistral-7b-openorca.Q4_K_M.gguf"
        model_path = hf_hub_download(model_name, filename=model_file)
        model_kwargs = {
        "n_ctx":4096,    # Context length to use
        "n_threads":16,   # Number of CPU threads to use
        "n_gpu_layers":33,# Number of model layers to offload to GPU. Set to 0 if only using CPU
        "verbose":False
        }
        return Llama(model_path=model_path, **model_kwargs)
    def __init__(self,base_brain) -> None:
        self.llm = base_brain
        self.prompt_token_counts = []
        self.generation_kwargs = {
            "max_tokens":256, # Max number of new tokens to generate
            "stop":["<|endoftext|>", "</s>","<|im_end|>","<|end|>","|<end","\n"], # Text sequences to stop generation on
            "echo":False, # Echo the prompt in the output
            "top_k":1, # This is essentially greedy decoding, since the model will always return the highest-probability token. Set this value > 1 for sampling decoding
            "temperature":0.2,
            "frequency_penalty":0.0,
            "repeat_penalty":1.1
        }
    def prompt(self,prompt_text:str):
        res = self.llm(prompt_text, **self.generation_kwargs)
        self.prompt_token_counts.append(res['usage']['prompt_tokens'])
        final_response = re.sub("\<\|[^\|]*\|\>","",res['choices'][0]['text']).strip()
        return final_response
    def is_this_a_question(self,statement):
        system_part = f"<|system|>\nYou only response with 'yes' or 'no'. Nothing else. Evaluate if what the user asks is a question.<|end|>"
        thought_part = f"<|user|>\nis this a question? '{statement}'<|end|>"
        full_prompt=  f"{system_part}\n{thought_part}\n<|assistant|>"
        res = self.llm(full_prompt)
        return re.sub("\<\|[^\|]*\|\>","",res['choices'][0]['text']).strip()
