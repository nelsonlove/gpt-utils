# gpt-utils

Helper tools for use with OpenAI's GPT-3 API.

The API key can be provided in three ways:
- In the environment variable `OPENAI_API_KEY`
- Via class attribute `GPT.api_key` of class `GPT` in module `gpt_utils.core` 
- Via keyword argument `api_key` in any method or function which obtains a response from OpenAI's servers 

## Disclaimer

These don't work perfectly.

## gpt_utils.utils

```
from gpt_utils import utils
```

`utils` contains simple functions which transform text in a specific way. Some functions are bidirectional; these take an optional **reverse** keyword argument which reverses the conversion's input and output.

### utils.case

```
>>> from gpt_utils.utils import case
```

Contains functions which modify the case of words in a string. These functions are meant to selectively preserve the case of proper nouns, etc. with minimal involvement. The first, `title()`, takes a `str` containing a word or phrase with proper capitalization for use in a heading or title: 

```
>>> case.title('the ant: an introduction')
'The Ant: An Introduction'
```

The second, `mid_sentence()`, adjusts the case of input words/phrases for insertion mid-sentence:

```
>>> case.mid_sentence('bicycles on inman street')
'bicycles on Inman Street'
>>> case.mid_sentence('An italian restaurant in somerville')
'an Italian restaurant in Somerville'
```

### utils.location

```
>>> from gpt_utils.utils import location
```

Currently contains one function, `fix_location()`, which takes an unformatted string containing a location and formats it properly for display:

```
>>> location.fix_location('lenox ma')
'Lenox, MA'
```

### utils.number

```
>>> from gpt_utils.utils import number
```

Contains two functions which convert numbers to strings.  The first, `number_to_str()`, takes an `int` or `float` and writes out the same number as a `str`:

```
>>> number.number_to_str(83)
'eighty-three'
>>> number.number_to_string(3.14)
'three point one four'
```

The second, `number_to_ordinal()`, takes an `int` and returns it in ordinal form as a `str`:

```
>>> number.number_to_ordinal(43)
'forty-third'
```

### utils.dechatify()

I have found that GPT tends to produce output of lower quality when it is prompted with text containing Internet/SMS vernacular. As a remedy, `dechatify()` converts text to standard/written English:

```
>>> utils.dechatify('how r u')
'How are you?'
>>> utils.dechatify('if the implementation is easy to explain then it might b a good idea')
'If the implementation is easy to explain, then it might be a good idea.'
```

### utils.generate_stem()

This function accepts a `str` containing a word/phrase and returns a sentence stem pairing the word/phrase with the appropriate form of the verb "to be":

```
>>> utils.generate_stem('GitHub')
'GitHub is'
>>> utils.generate_stem("pleiades")
'The Pleiades are'
```