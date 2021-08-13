import abc

from transformers import GPT2Tokenizer

from .core import GPT


class BasePrompt(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def text(self):
        raise NotImplementedError

    def tokens(self, *args, **kwargs):
        if not args or kwargs:
            text = self.text
        else:
            text = self.text.format(*args, **kwargs)
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
        return tokenizer.tokenize(text)

    def __str__(self):
        return self.text

    def format(self, *args, **kwargs):
        return self.text.format(*args, **kwargs)


class ExamplesPrompt(BasePrompt, metaclass=abc.ABCMeta):
    def __init__(self,
                 *examples,            # Sequence of examples used to build prompt
                 labels=None,          # List of labels used for each example
                 intro_text=None,      # Text inserted at beginning of prompt
                 auto_truncate=False,  # If true, truncate if prompt goes over max_tokens
                 max_tokens=2048,
                 ):
        self.examples = examples
        self.labels = labels
        self.intro_text = intro_text
        self.auto_truncate = auto_truncate
        self.max_tokens = max_tokens

    def truncate(self):
        self.examples = self.examples[1:]

    @property
    def text(self):
        def format_example_str(ex):
            if type(ex) is str:
                return (self.labels[0] if self.labels else '') + ex + '\n'
            else:
                example_str = ''
                for i, item in enumerate(ex):
                    example_str += (self.labels[i] + ' ' if self.labels else '') + item + '\n'
                return example_str

        is_seq = type(self.examples[0]) is not str

        prompt = self.intro_text + '\n\n' if self.intro_text else ''

        for example in self.examples:
            prompt += format_example_str(example)
            if is_seq:
                prompt += '\n'

        if is_seq and self.labels:
            for label in self.labels[:-1]:
                prompt += label + ' {}\n'
            prompt += self.labels[-1]
        elif self.labels:
            prompt += self.labels[0]

        return prompt.strip()

    def format(self, *args, **kwargs):
        formatted = self.text.format(*args, **kwargs)
        while self.auto_truncate and len(formatted) <= self.max_tokens:
            self.truncate()
            formatted = self.text.format(*args, **kwargs)
        return formatted


class ConversionPrompt(ExamplesPrompt):
    def __init__(self,
                 in_label,
                 out_label,
                 *examples,
                 intro_text=None,
                 auto_truncate=False,
                 max_tokens=2048,
                 response_max_tokens=100,
                 **kwargs               # kwargs here are passed to GPT with some defaults
                 ):
        super().__init__(*examples,
                         labels=[in_label + ':', out_label + ':'],
                         intro_text=intro_text,
                         auto_truncate=auto_truncate,
                         max_tokens=max_tokens)

        if 'temperature' not in kwargs:
            kwargs['temperature'] = 0.1

        if 'stop' not in kwargs:
            kwargs['stop'] = '\n'

        self.gpt = GPT(max_tokens=response_max_tokens, **kwargs)

    @GPT.requires_key
    def convert(self, in_text, reverse=False):
        """Formats prompt and translates in_text. Optionally takes a
        reverse argument which temporarily switches inputs and outputs"""
        original_examples = self.examples
        original_labels = self.labels
        if reverse:
            self.examples = [(example[1], example[0]) for example in self.examples]
            self.labels = (self.labels[1], self.labels[0])
        response = self.gpt.response(self.format(in_text))
        if reverse:
            self.examples = original_examples
            self.labels = original_labels
        return response
