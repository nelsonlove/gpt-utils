from unittest import TestCase

from gpt_utils import utils


class Test(TestCase):
    def assert_transform(self, func, input_str, output_str):
        self.assertEqual(func(input_str), output_str)

    def test_dechatify(self):
        self.assert_transform(utils.dechatify, 'lol', 'Laughing out loud.')

    def test_fix_case(self):
        self.assert_transform(utils.dechatify, "Pigeon Racing", "pigeon racing")

    def test_leetify(self):
        self.assert_transform(utils.leetify, 'Nice to meet you.', 'nic3 t0 m33t j00.')
