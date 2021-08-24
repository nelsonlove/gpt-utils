from . import GPT
from .prompt import ConversionPrompt


@GPT.requires_key
def mid_sentence(in_text):
    """Returns a word or phrase with proper capitalization for insertion mid-sentence"""
    prompt = ConversionPrompt(
        'I', 'O',
        ("the fbi", "the FBI"),
        ("hall and oates", "Hall and Oates"),
        ("Pigeon Racing", "pigeon racing"),
        ("The President", "the President"),
        ("st mary", "St. Mary"),
        ("a history of western philosophy", "a history of Western philosophy"),
        intro_text="Demonstrate the proper capitalization/punctuation for the phrase as it"
                   "would be used mid-sentence. The first letter should not be capitalized unless it is part of a "
                   "proper noun or phrase.",
        max_tokens=20)
    return prompt.convert(in_text)


@GPT.requires_key
def title(text):
    """Returns a word or phrase with proper capitalization for use in a heading or title"""
    prompt = ConversionPrompt(
        'I', 'O',
        ("duck", "Duck"),
        ("Alarm Clock", "Alarm clock"),
        ("the fbi", "FBI"),
        ("hall and oates", "Hall and Oates"),
        ("pigeon racing", "Pigeon racing"),
        ("Gemstones", "Gemstones"),
        ("mangoes", "Mangoes"),
        ("st mary", "St. Mary"),
        ("a history of western philosophy", "A History of Western Philosophy"),
        temperature=0.01,
        intro_text="Demonstrate the proper capitalization/punctuation for the phrase as it would be used in a heading "
                   "or title.",
        max_tokens=20,
        engine='curie')
    return prompt.convert(text)
