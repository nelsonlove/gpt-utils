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
                              engine='ada',
                              temperature=0.1,
                              intro_text="Capitalize and retain case.")

    return prompt.convert(noun)
