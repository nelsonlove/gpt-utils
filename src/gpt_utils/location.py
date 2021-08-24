from . import GPT
from .prompt import ConversionPrompt


@GPT.requires_key
def fix_location(in_text):
    """Accepts a string containing a location and formats it properly."""
    prompt = ConversionPrompt(
        'I', 'O',
        ("lenox ma", "Lenox, MA"),
        ("london", "London, U.K."),
        ("chicago", "Chicago, IL"),
        ("dallas, tx", "Dallas, TX"),
        engine='babbage'
    )
    return prompt.convert(in_text)
