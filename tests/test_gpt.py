from unittest import TestCase

from gpt_utils import GPT


class Test(TestCase):
    def test_gpt_completion(self):
        completion = GPT(max_tokens=2, temperature=0.0).response("The best things in life")
        self.assertIsNot(completion, "are")
