from unittest import TestCase

from gpt_utils import utils


class Test(TestCase):
    def assert_transform(self, func, input_str, output_str):
        self.assertEqual(func(input_str), output_str)

    def test_dechatify(self):
        self.assert_transform(utils.dechatify, 'lol', 'Laughing out loud.')

    def test_fix_case(self):
        self.assert_transform(utils.fix_case, 'a japanese restaurant', 'a Japanese restaurant')

    def test_generate_stem(self):
        self.assert_transform(utils.generate_stem, "White House", "The White House is")

    def test_leetify(self):
        self.assert_transform(utils.leetify, 'Nice to meet you.', 'nic3 t0 m33t j00.')
