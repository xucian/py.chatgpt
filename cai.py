import tiktoken

# OPEN_AI_COMPLETION_MODEL = 'text-davinci-002'
# newer model as of 26.12.2022
OPEN_AI_COMPLETION_MODEL = 'text-davinci-003'

_TOKEN_ENCODER = tiktoken.get_encoding("gpt2")

_MAX_TOKENS = 4096
MAX_TOKENS_SAFE = int(_MAX_TOKENS * 0.97)


def convert_words_to_tokens(words: int):
	"""
	Based on this blog post: https://towardsdatascience.com/chatgpt-and-dall-e-2-in-a-panel-app-1c921d7d9021
	And fromt he official tokenizer tool: https://beta.openai.com/tokenizer?view=bpe
	"""
	return int(words * 1.25)


def convert_string_to_tokens(text: str):
	return _TOKEN_ENCODER.encode(text)


def convert_string_to_num_tokens(text: str):
	return len(convert_string_to_tokens(text))


def get_max_tokens_param(max_words: int, prompt: str):
	prompt_tokens = convert_string_to_num_tokens(prompt)
	max_tokens_provided = convert_words_to_tokens(max_words)
	max_tokens_considering_prompt_length = MAX_TOKENS_SAFE - prompt_tokens

	return min(max_tokens_provided, max_tokens_considering_prompt_length)
