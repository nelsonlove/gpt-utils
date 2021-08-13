# gpt-utils

Helper tools for use with OpenAI's GPT-3 API.

The API key can be provided in three ways:
- In the environment variable **OPENAI_API_KEY**
- By importing the **GPT** class from **gpt_utils.core** and setting GPT.api_key
- By passing the key as keyword argument **api_key** to any method which obtains a response from OpenAI's servers 

## gpt_utils.utils

```
from gpt_utils import utils
```

**utils** contains simple functions which transform text in a specific way. Some functions are bidirectional; these take an optional **reverse** keyword argument which reverses the conversion's input and output.


### utils.generate_stem()

Accepts a string containing a word/phrase and returns a sentence stem pairing the word/phrase with the appropriate form of the verb "to be":

```
>>> utils.generate_stem('GitHub')
'GitHub is'

>>> utils.generate_stem("pleiades")
'The Pleiades are'
```

### utils.fix_case()

Adjusts case of input words/phrases for insertion mid-sentence:

```
>>> utils.fix_case('bicycles on inman street')
'bicycles on Inman Street'

>>> utils.fix_case('An italian restaurant in Somerville')
'an Italian restaurant in Somerville'
```

### utils.dechatify()

Converts Internet/SMS vernacular to standard/written English. Takes an optional **reverse** keyword argument which, if true, causes the function to convert from standard English to Internet/SMS speak:

```
>>> utils.dechatify('how r u')
'How are you?'

>>> utils.dechatify("If the implementation is easy to explain, it may be a good idea.", reverse=True)
'if the implementation is easy to explain, it may be a good idea'
```