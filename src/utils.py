from gpt import GPT, TuplePrompt


def strip_quotes(text):
    if text and text[0] == text[-1] and text[0] in ['"', "'"]:
        quote = text[0]
        text = text.strip(quote)
    return text


@GPT.requires_key
def leetify(message):
    examples = (
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
         'nic3 t0 m33t j00.')
    )
    prompt = TuplePrompt(
        examples,
        'Standard American English',
        'l33tsp34k'
    ).format(message)
    return GPT(max_tokens=100, stop='\n', temperature=0.1).response(prompt)


@GPT.requires_key
def dechatify(message):
    examples = (
        ('please provide me with a short brief',
         'Please provide me with a short brief.'),
        ('It\'s working',
         'It\'s working.'),
        ('yeah',
         'Yeah.'),
        ('lol',
         'Laughing out loud.'),
        ('omg',
         'Oh my god.'),
        ('How goes it',
         'How goes it?')
    )
    prompt = TuplePrompt(
        examples,
        'Internet/SMS English',
        'Standard American English',
    ).format(message)
    return GPT(max_tokens=100, stop='\n', temperature=0.1).response(prompt)
