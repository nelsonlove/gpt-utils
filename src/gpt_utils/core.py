import os

import openai


class GPT:
    """Base object for GPT-3 completions"""

    api_key = os.environ.get('OPENAI_API_KEY')

    @classmethod
    def requires_key(cls, func):
        """Decorator function which allows passing API key as keyword argument"""
        def wrapped(*args, api_key=None, **kwargs):
            if api_key:
                cls.api_key = api_key
            return func(*args, **kwargs)

        return wrapped

    def __init__(self,
                 engine='davinci',
                 max_tokens=512,
                 temperature=0.5,
                 top_p=1,
                 n=1,
                 stream=False,
                 logprobs=None,
                 echo=False,
                 stop=None,
                 presence_penalty=0,
                 frequency_penalty=0,
                 best_of=1,
                 logit_bias=None,
                 log_file=None
                 ):

        openai.api_key = self.api_key

        self.engine = engine
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.n = n
        self.stream = stream
        self.logprobs = logprobs
        self.echo = echo
        self.stop = stop
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.best_of = best_of
        self.logit_bias = logit_bias or {}

        self.history = []
        self.log_file = log_file

    def response(self, prompt, on_fail=None, api_key=None, max_attempts=3):
        if api_key:
            self.api_key = api_key
        openai.api_key = self.api_key

        response = None
        while max_attempts and not response:
            try:
                response = self._response(prompt)
            except openai.error.InvalidRequestError:
                if not on_fail:
                    raise
                else:
                    response = on_fail(prompt)
            max_attempts -= 1

        self.history.append((prompt, response))

        if self.log_file:
            with open(self.log_file, 'w') as f:
                # TODO Logging format should be JSON or some other format that makes sense, as a matter of fact
                #  logging could use some work all around
                f.write(f'[PROMPT]\n\n{prompt}\n\n[RESPONSE]\n\n{response}\n\n')

        return response

    def _response(self, prompt):
        return openai.Completion.create(prompt=str(prompt),
                                        engine=self.engine,
                                        max_tokens=self.max_tokens,
                                        temperature=self.temperature,
                                        top_p=self.top_p,
                                        n=self.n,
                                        stream=self.stream,
                                        logprobs=self.logprobs,
                                        echo=self.echo,
                                        stop=self.stop,
                                        presence_penalty=self.presence_penalty,
                                        frequency_penalty=self.frequency_penalty,
                                        best_of=self.best_of,
                                        logit_bias=self.logit_bias)['choices'][0]['text'].strip()
