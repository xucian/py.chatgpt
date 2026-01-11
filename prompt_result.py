class PromptResult:
    def __init__(self, resp):
        self.resp = resp

    def __str__(self):
        # For ChatCompletion, we need to access the message content
        if hasattr(self.resp, 'choices') and len(self.resp.choices) > 0:
            return self.resp.choices[0].message.content
        return str(self.resp)