import openai
import os


OPENAI_KEY = os.environ.get('OPENAI_KEY')


def set_openai_key(key):
    global OPENAI_KEY
    OPENAI_KEY = key


def requires_key(func):
    def wrapped(*args, openai_key=None, **kwargs):
        if openai_key:
            set_openai_key(openai_key)
        return func(*args, **kwargs)
    return wrapped


class GPT:
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
                 **kwargs
                 ):
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

    def response(self, prompt):
        response = openai.Completion.create(prompt=str(prompt),
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
        self.history.append((prompt, response))
        return response


class TuplePrompt:
    def __init__(self,
                 tuples,
                 input_label='Q',
                 output_label='A',
                 intro_text=None,
                 spacing=2
                 ):
        self.tuples = tuples
        self.input_label = input_label
        self.output_label = output_label
        self.intro_text = intro_text
        self.spacing = spacing

    @property
    def spacer(self):
        return '\n' * self.spacing

    def tuple_to_str(self, t):
        return f'{self.input_label}: {t[0]}\n{self.output_label}: {t[1]}'

    def format(self, text):
        return str(self).format(text)

    def __str__(self):
        text = self.intro_text + self.spacer if isinstance(self.intro_text, str) else ''
        text += self.spacer.join(self.tuple_to_str(t) for t in self.tuples)
        text += self.spacer + f'{self.input_label}: {"{}"}\n' + f'{self.output_label}:'
        return text
