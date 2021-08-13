from gpt_utils import GPT
from gpt_utils.prompt import ConversionPrompt


@GPT.requires_key
def generate_stem(in_text):
    """Returns a sentence stem containing the word or phrase and
    the appropriate form of the verb "to be"."""
    prompt = ConversionPrompt(
        'I', 'O',
        ("Golf", "Golf is..."),
        ("Beetles", "Beetles are..."),
        ("White House", "The White House is..."),
        ("Associate professor", "An associate professor is..."),
        ("Beatles", "The Beatles were..."),
        ("Murder of Crows", "A murder of crows is..."),
        ("battle of hastings", "The Battle of Hastings was..."),
        intro_text="Demonstrate how to use the phrase at the beginning of a sentence."
                   "Make sure to use the entire phrase.",
        stop='...',
    )
    return prompt.convert(in_text)
