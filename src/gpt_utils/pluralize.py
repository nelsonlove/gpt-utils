from . import GPT
from .prompt import ConversionPrompt


@GPT.requires_key
def pluralize(noun):
    prompt = ConversionPrompt('Singular', 'Plural',
                              ('whale', 'whales'),
                              ('Ox', 'Oxen'),
                              ('moose', 'Moose'),
                              ('MOOSE', 'MOOSE'),
                              ('bear', 'bears'),
                              ('Squirrel', 'Squirrels'),
                              ('Fire hydrant', 'Fire hydrants'),
                              engine='babbage',
                              temperature=0.1,
                              intro_text="For each singular noun, provide the plural and retain case.")
    print(prompt)
    return prompt.convert(noun)
