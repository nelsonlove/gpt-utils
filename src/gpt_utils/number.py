from . import GPT
from .prompt import ConversionPrompt


@GPT.requires_key
def number_to_str(number):
    """Convert an int or float to words."""
    prompt = ConversionPrompt(
        'Number', 'String',
        ("3", "three"),
        ("8", "eight"),
        ("3.9", "three point nine"),
        ("0.5", "zero point five"),
        ("19", "nineteen"),
        ("49", "forty-nine"),
        ("100", "one hundred"),
        ("57", "fifty-seven"),
        ("12", "twelve"),
        temperature=0.01,
        max_tokens=5,
        engine='curie')
    return prompt.convert(str(number))


@GPT.requires_key
def number_to_ordinal(number):
    """Convert an int of an ordinal number to a string."""
    prompt = ConversionPrompt(
        'Number', 'String',
        ("3", "third"),
        ("8", "eighth"),
        ("1", "first"),
        ("12", "twelfth"),
        ("48", "forty-eighth"),
        temperature=0.01,
        max_tokens=5,
        engine='babbage')
    return prompt.convert(str(number))
