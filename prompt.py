from typing import Optional

class Prompt:
    def __init__(self, ai_prompt: str, approx_words: Optional[int], approx_max_words: int, creativity01: float,
                 stream_output: bool):
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