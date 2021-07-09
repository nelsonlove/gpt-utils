from unittest import TestCase


import gpt_utils


class Test(TestCase):
    def assert_transform(self, func, input_str, output_str):
        self.assertEqual(func(input_str), output_str)

    def test_dechatify(self):
        self.assert_transform(gpt_utils.dechatify, 'lol', 'Laughing out loud.')

    def test_leetify(self):
        self.assert_transform(gpt_utils.leetify, 'Nice to meet you.', 'nic3 t0 m33t j00.')

    def test_strip_quotes(self):
        self.assert_transform(gpt_utils.strip_quotes, '"Hello!"', 'Hello!')
