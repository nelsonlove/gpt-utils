from unittest import TestCase

from gpt_utils import GPT


class Test(TestCase):
    def test_gpt_completion(self):
        completion = GPT(max_tokens=2).response("What's up?")
        self.assertIsNot(completion, "")
