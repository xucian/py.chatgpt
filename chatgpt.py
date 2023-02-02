"""
Generate a script from questions

"""
import os
from datetime import date

import openai
from dotenv import load_dotenv

import cai


load_dotenv()  # take environment variables from .env.


class ChatGptPrompt:
    def __init__(self, ai_prompt: str, approx_words: int | None, approx_max_words: int, creativity01: float,
                 stream_output: True):
        """
        :param ai_prompt:
        :param approx_words:
        :param approx_max_words:
        :param creativity01: 0 means more exact answers, 1 means full creativity and novelty, also gives different
            answers each time (it adds entropy)
        """
        self.ai_prompt = ai_prompt
        self.approx_words = approx_words
        self.approx_max_words = approx_max_words
        self.creativity01 = creativity01
        self.stream_output = stream_output

    def __str__(self):
        return f'[' \
               f'approx_max_words={self.approx_max_words}, ' \
               f'creativity01={self.creativity01}, ' \
               f'stream_output={self.stream_output}, ' \
               f']:\n' \
               f'{self.ai_prompt}'


class ChatGptPromptResult:
    def __init__(self, resp):
        self.resp = resp

    def __str__(self):
        return self.resp.choices[0].text


class ChatGptGen:
    def __init__(self, user_hint: str):
        self.user_hint = user_hint

    def gen(self, prompt: ChatGptPrompt) -> ChatGptPromptResult:

        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = self.__request(prompt)
        return ChatGptPromptResult(response)

    def __request(self, prompt: ChatGptPrompt):
        response = openai.Completion.create(
            model=cai.OPEN_AI_COMPLETION_MODEL,
            prompt=self.__generate_para_prompt_text(prompt),
            temperature=prompt.creativity01,

            # 1 by default, but making it explicit and safe-guarding for future API changes
            n=1,

            # 16 is default, 4096 is max (for new models)
            # max_tokens=16,
            max_tokens=cai.get_max_tokens_param(prompt.approx_max_words, prompt.ai_prompt),

            # [-2.0, 2.0]. 0.0 by default. Positive values make it go on less tangents in the conversation
            # A likely analogy: presence_penalty works on meaning while frequency_penalty on verbatim constructs
            # https://beta.openai.com/docs/api-reference/parameter-details
            presence_penalty=0.1,

            # [-2.0, 2.0]. 0.0 by default. See presence_penalty
            frequency_penalty=0.1,

            # False by default
            stream=prompt.stream_output,

            # 1 by default. Could increase accuracy, but linearly increases costs
            best_of=1,

            # uid of the end-user. optional
            user=self.user_hint,

            # Use the tokenizer tool at https://beta.openai.com/tokenizer?view=bpe to
            #   TODO there's an API on that page
            # Map example: {"50256": -1} to
            # Bias in [-100, 100]
            # Use values in [-1, 1] to change the likelihood of a token, and bigger values for a ban or
            # exclusive-selection (respectively). So values in [-1, 1] aren't actual probabilities, but biases
            logit_bias={}
        )

        return response

    # noinspection PyMethodMayBeStatic
    def __generate_para_prompt_text(self, prompt: ChatGptPrompt):
        if prompt.approx_words is None:
            return prompt.ai_prompt

        return f'Answer in about {prompt.approx_words} words: {prompt.ai_prompt}'


if __name__ == '__main__':

    gen = ChatGptGen(user_hint='chatgpt_console_test')

    ai_name = 'ChatGPT'
    # ai_name = 'Cassandra'
    intro = f"You are {ai_name}, a large language model trained by OpenAI. You answer as concisely as " \
            f"possible for each response, unless otherwise specified or the number of words is specified. " \
            f"If you are generating a list, do not have too many items. Keep the number of items short. " \
            f"Knowledge cutoff: 2021-09, " \
            f"Current date: {str(date.today())}"
    # intro = f"Your name is {ai_name}."
    intro = f"{intro}\n\n" \
            f"Below is a past conversation between us. Please complete it:\n\n"

    history = []

    while True:
        message = input('You: ')
        if message == 'exit':
            break

        full_prompt = ''
        full_prompt += intro
        full_prompt += '\n'.join([
            f'Me: {h["user"]}\n'
            f'You: {h["ai"]}\n'  # extra line-break between Q:A pairs
            for h in history
        ])
        full_prompt += f'Me: {message}\n'
        full_prompt += f'You: \n'
        history_tc = cai.convert_string_to_num_tokens(full_prompt)
        response_approx_max_words = 500
        response_approx_max_tokens = cai.convert_words_to_tokens(response_approx_max_words)
        # TODO always add the first paras (instructions on who are we etc.), add the fact that there's some missing
        #  info etc.
        total_tokens = history_tc + response_approx_max_tokens
        if total_tokens > cai.MAX_TOKENS_SAFE:
            surplus_tokens = total_tokens - cai.MAX_TOKENS_SAFE
            surplus_tokens_ratio = surplus_tokens / cai.MAX_TOKENS_SAFE
            surplus_nchars = round(len(full_prompt) * surplus_tokens_ratio)

            # TODO
            conv_cut_explanation = f"[This part was removed]\n\n"

            full_prompt = full_prompt[-surplus_nchars:]

        p = ChatGptPrompt(full_prompt, approx_words=None, approx_max_words=response_approx_max_words, creativity01=0.5,
                          stream_output=True)

        try:
            result = gen.gen(p)
        except Exception as e:
            print(e)
            print(f'[Sorry, that didn\'t work. Please try again:]')
            continue

        resp_text_so_far = ''
        print(f'{ai_name}: ', end='')

        try:
            for part in result.resp:
                resp_text = part.choices[0].text
                resp_text_so_far += resp_text
                print(resp_text, end='')
        except Exception as e:
            print(e)
            print(f'[Sorry, something interrupted the response. Please try again]')
            continue

        history.append({'user': message, 'ai': resp_text_so_far})
        print('\n')
