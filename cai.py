import os
import tiktoken
from typing import Optional

# OpenAI API constants
OPEN_AI_COMPLETION_MODEL = "gpt-3.5-turbo"

# Token constants
MAX_TOKENS_SAFE = 4096

# Initialize the tokenizer
_TOKEN_ENCODER = tiktoken.encoding_for_model("gpt-3.5-turbo")

def convert_words_to_tokens(words: int):
    """
    Based on this blog post: https://towardsdatascience.com/chatgpt-and-dall-e-2-in-a-panel-app-1c921d7d9021
    And from the official tokenizer tool: https://beta.openai.com/tokenizer?view=bpe
    """
    return int(words * 1.25)

def convert_string_to_num_tokens(text: str):
    return len(convert_string_to_tokens(text))

def convert_string_to_tokens(text: str):
    return _TOKEN_ENCODER.encode(text)

def get_max_tokens_param(max_words: int, prompt: str):
    prompt_tokens = convert_string_to_num_tokens(prompt)
    max_tokens_provided = convert_words_to_tokens(max_words)
    max_tokens_considering_prompt_length = MAX_TOKENS_SAFE - prompt_tokens

    return min(max_tokens_provided, max_tokens_considering_prompt_length)