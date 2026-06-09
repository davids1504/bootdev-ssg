import unittest

from generate_page import extract_title


class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        markdown = "test/test.md"
        expected_result = "Test"
        self.assertEqual(expected_result, extract_title(markdown))

    def test_extract_title_multi_word(self):
        markdown = "test/test_mw.md"
        expected_result = "Test Multiword"
        self.assertEqual(expected_result, extract_title(markdown))
