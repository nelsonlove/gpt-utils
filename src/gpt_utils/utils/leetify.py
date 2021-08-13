from gpt_utils import GPT
from gpt_utils.prompt import ConversionPrompt


@GPT.requires_key
def leetify(in_text, reverse=False):
    prompt = ConversionPrompt(
        'American English', 'l33tsp34k',
        ('Please provide me with a short brief.',
         'plz giev sh0rt br13f.'),
        ('It\'s working.',
         'its w0rk1n9.'),
        ('yeah',
         'y34h.'),
        ('lol',
         'l0l.'),
        ('omg',
         'omg'),
        ('How are you?',
         'sup n00b'),
        ('the universe',
         'th3 j00n1v3rs3'),
        ('Nice to meet you.',
         'nic3 t0 m33t j00.'),
    )
    return prompt.convert(in_text, reverse=reverse)
