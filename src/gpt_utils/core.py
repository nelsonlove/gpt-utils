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
                openai.api_key = cls.api_key
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

    def response(self, prompt, on_fail=None, max_attempts=3, text_only=True, preview=False, api_key=None):
        if api_key:
            self.__class__.api_key = api_key
            openai.api_key = self.api_key

        response = None

        while max_attempts and not response:
            try:
                response = self._response(prompt, preview=preview)
            except openai.error.InvalidRequestError:
                if not on_fail:
                    raise
                else:
                    return on_fail(prompt)
            max_attempts -= 1

        response_text = response['choices'][0]['text'].strip()

        if preview:
            print(f'Response: {response_text}')

        self.history.append((prompt, response_text))

        if self.log_file:
            with open(self.log_file, 'w') as f:
                # TODO Logging format should be JSON or some other format that makes sense, as a matter of fact
                #  logging could use some work all around
                f.write(f'[PROMPT]\n\n{prompt}\n\n[RESPONSE]\n\n{response_text}\n\n')

        return response_text if text_only else response

    def _response(self, prompt, preview=False):
        prompt = str(prompt).strip()

        if preview:
            excerpt = prompt[:min(60, len(prompt))]
            print(f'Querying with prompt: {excerpt + ("..." if len(prompt) > 60 else "")}')

        return openai.Completion.create(prompt=prompt,
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
                                        logit_bias=self.logit_bias)
