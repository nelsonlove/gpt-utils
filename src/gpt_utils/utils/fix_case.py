from gpt_utils import GPT
from gpt_utils.prompt import ConversionPrompt


@GPT.requires_key
def fix_case(in_text):
    """Returns a word or phrase with proper capitalization for insertion mid-sentence"""
    prompt = ConversionPrompt(
        'I', 'O',
        ("the fbi", "the FBI"),
        ("hall and oates", "Hall and Oates"),
        ("Pigeon Racing", "pigeon racing"),
        ("The President", "the President"),
        ("st mary", "St. Mary"),
        intro_text="Demonstrate the proper capitalization/punctuation for the phrase as it"
                   "would be used mid-sentence.",
    )
    return prompt.convert(in_text)
