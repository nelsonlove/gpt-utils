from gpt_utils import GPT
from gpt_utils.prompt import ConversionPrompt


@GPT.requires_key
def dechatify(in_text, reverse=False):
    """Converts Internet/SMS vernacular to standard/written English, or vice versa"""
    prompt = ConversionPrompt(
        'Internet/SMS', 'Standard/Written',
        ('please provide me with a short brief',
         'Please provide me with a short brief.'),
        ('its working',
         'It\'s working.'),
        ('yeah',
         'Yeah.'),
        ('lol',
         'Laughing out loud.'),
        ('omg',
         'Oh my god.'),
        ('how goes it',
         'How goes it?'),
    )
    return prompt.convert(in_text, reverse=reverse)
