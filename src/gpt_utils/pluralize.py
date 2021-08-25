from . import GPT
from .prompt import ConversionPrompt


@GPT.requires_key
def pluralize(noun):
    prompt = ConversionPrompt('Singular', 'Plural',
                              ('whale', 'whales'),
                              ('Ox', 'Oxen'),
                              ('moose', 'moose'),
                              ('MOOSE', 'MOOSE'),
                              ('bear', 'bears'),
                              ('Squirrel', 'Squirrels'),
                              ('Fire hydrant', 'Fire hydrants'),
                              engine='curie',
                              temperature=0.05,
                              intro_text="For each singular noun, provide the plural. Retain the case of the original.")
    return prompt.convert(noun)
