from gpt_utils import utils


from unittest import TestCase


class Test(TestCase):
    def assert_transform(self, func, input_str, output_str):
        self.assertEqual(func(input_str), output_str)

    def test_dechatify(self):
        self.assert_transform(util.dechatify, 'lol', 'Laughing out loud.')

    def test_leetify(self):
        self.assert_transform(util.leetify, 'Nice to meet you.', 'nic3 t0 m33t j00.')
