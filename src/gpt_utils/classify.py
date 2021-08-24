from . import GPT


def content(text, toxic_threshold=-0.355):
    """Uses OpenAI's content filter engine to classify text as safe or unsafe. Essentially unmodified from OpenAI's
    example at https://beta.openai.com/docs/engines/content-filter:

    "The filter aims to detect generated text that could be sensitive or unsafe coming from the API. It's currently in
    beta mode and has three ways of classifying text- as safe, sensitive, or unsafe. The filter will make mistakes and
    we have currently built it to err on the side of caution, thus, resulting in higher false positives."

    This function accepts a str, `text`, and returns a str of "0", "1", or "2", indicating the likelihood that `text`
    is unsafe. The function also takes an optional float, `threshold`, the probability at which a "2" from GPT is taken
    to be real and not a false positive.

    Explanations for the function's possible responses (from the URL above):

    0 - The text is safe.
    1 - This text is sensitive. This means that the text could be talking about a sensitive topic, something political,
        religious, or talking about a protected class such as race or nationality.
    2 - This text is unsafe. This means that the text contains profane language, prejudiced or hateful language,
        something that could be NSFW, or text that portrays certain groups/people in a harmful manner.
    """
    response = GPT(
        engine="content-filter-alpha-c4",
        temperature=0,
        max_tokens=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        logprobs=10
    ).response("<|endoftext|>" + text + "\n--\nLabel:", text_only=False)

    output_label = response["choices"][0]["text"]

    if output_label == "2":
        # If the model returns "2", return its confidence in 2 or other output-labels
        logprobs = response["choices"][0]["logprobs"]["top_logprobs"][0]

        # If the model is not sufficiently confident in "2",
        # choose the most probable of "0" or "1"
        # Guaranteed to have a confidence for 2 since this was the selected token.
        if logprobs["2"] < toxic_threshold:
            logprob_0 = logprobs.get("0", None)
            logprob_1 = logprobs.get("1", None)

            # If both "0" and "1" have probabilities, set the output label
            # to whichever is most probable
            if logprob_0 is not None and logprob_1 is not None:
                if logprob_0 >= logprob_1:
                    output_label = "0"
                else:
                    output_label = "1"
            # If only one of them is found, set output label to that one
            elif logprob_0 is not None:
                output_label = "0"
            elif logprob_1 is not None:
                output_label = "1"

            # If neither "0" or "1" are available, stick with "2"
            # by leaving output_label unchanged.

    # if the most probable token is none of "0", "1", or "2"
    # this should be set as unsafe
    if output_label not in ["0", "1", "2"]:
        output_label = "2"

    return output_label
