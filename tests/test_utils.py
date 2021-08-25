from unittest import TestCase

import gpt_utils


class Test(TestCase):
    def assert_transform(self, func, input_str, output_str):
        self.assertEqual(output_str, func(input_str))

    def test_dechatify(self):
        self.assert_transform(gpt_utils.dechatify, 'lol', 'Laughing out loud.')

    def test_leetify(self):
        self.assert_transform(gpt_utils.leetify, 'Nice to meet you.', 'nic3 t0 m33t j00.')

    def test_pluralize(self):
        self.assert_transform(gpt_utils.pluralize, 'lion', 'lions')
        self.assert_transform(gpt_utils.pluralize, 'Peach', 'Peaches')
        self.assert_transform(gpt_utils.pluralize, 'CHILD', 'CHILDREN')
        self.assert_transform(gpt_utils.pluralize, 'Tuba', 'Tubas')

    def test_case_title(self):
        self.assert_transform(gpt_utils.case.title, 'a japanese restaurant', 'A Japanese Restaurant')

    def test_case_mid_sentence(self):
        self.assert_transform(gpt_utils.case.mid_sentence, 'a japanese restaurant', 'a Japanese restaurant')

    def test_generate_stem(self):
        self.assert_transform(gpt_utils.generate_stem, "White House", "The White House is")

    def test_number_to_str(self):
        self.assert_transform(gpt_utils.number.number_to_str, 34, 'thirty-four')
        self.assert_transform(gpt_utils.number.number_to_str, 34.3, 'thirty-four point three')

    def test_number_to_ordinal(self):
        self.assert_transform(gpt_utils.number.number_to_ordinal, 14, 'fourteenth')
