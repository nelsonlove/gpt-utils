import abc
import json

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


class ExamplesPrompt(BasePrompt):
    def __init__(self,
                 *examples,            # Sequence of examples used to build prompt
                 labels=None,          # List of labels used for each example
                 intro_text=None,      # Text inserted at beginning of prompt
                 auto_truncate=False,  # If true, truncate if prompt goes over max_tokens
                 max_tokens=2048,
                 ):
        self.examples = list(examples)
        self.labels = labels
        self.intro_text = intro_text
        self.auto_truncate = auto_truncate
        self.max_tokens = max_tokens

    def truncate(self):
        self.examples = self.examples[1:]

    def _format_example_str(self, example):
        if type(example) is str:
            return (self.labels[0] if self.labels else '') + example + '\n'
        else:
            example_str = ''
            for i, item in enumerate(example):
                example_str += (self.labels[i] + ' ' if self.labels else '') + item + '\n'
            return example_str

    @property
    def text(self):
        is_seq = type(self.examples[0]) is not str

        prompt = self.intro_text + '\n\n' if self.intro_text else ''

        for example in self.examples:
            prompt += self._format_example_str(example)
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
        while self.auto_truncate and len(formatted) > self.max_tokens:
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


class MatrixPrompt(BasePrompt):
    @classmethod
    def load(cls, file):
        """Accepts path to a .json file and returns a list of dicts, one for each row"""
        with open(file, newline='') as f:
            return json.load(f)

    def __init__(self, data,
                 output_column=None,
                 input_columns=None,
                 label_delimiter=': ',
                 intro_text=None):
        self.data = self.load(data) if not isinstance(data, dict) else data
        self.columns = list(self.data[0].keys())
        self.output_column = output_column or []
        self.input_columns = input_columns or []
        self.label_delimiter = label_delimiter
        self.intro_text = intro_text

    def _format_example_str(self, example):
        example_str_list = []
        for label, value in example:
            if type(value) is list:
                value = '|'.join(value)
            example_str = f'{label}{self.label_delimiter}{value}'
            example_str_list.append(example_str)
        return '\n'.join(example_str_list)

    def _example_from_row(self, row):
        return [[col, row[col]] for col in self.input_columns + [self.output_column]]

    @property
    def examples(self):
        return [self._example_from_row(row) for row in self.data]

    @property
    def text(self):
        prompt = self.intro_text + '\n\n' if self.intro_text else ''

        for example in self.examples:
            prompt += self._format_example_str(example) + '\n\n'

        for col in self.input_columns:
            prompt += col + self.label_delimiter + '{}' + '\n'

        prompt += self.output_column + self.label_delimiter

        return prompt.strip()

    @staticmethod  # I should move this somewhere, it doesn't make sense here
    def split_list(l_string, delimiter='|'):
        if delimiter not in l_string and 'none' in l_string.lower():
            return ['None']
        else:
            return [item.strip() for item in l_string.split(delimiter)]

    @GPT.requires_key
    def predict(self, *input_values,
                as_list=False,
                list_delimiter='|',
                uniques_only=False,
                **gpt_kwargs
                ):
        if not self.output_column:
            raise Exception('Need to set output column!')

        if 'stop' not in gpt_kwargs:
            gpt_kwargs['stop'] = '\n'
        gpt = GPT(**gpt_kwargs)

        prompt = self.format(*input_values)
        response = gpt.response(prompt)
        if not as_list:
            return response
        else:
            response_list = self.split_list(response, list_delimiter)
            return list(set(response_list)) if uniques_only else response_list
