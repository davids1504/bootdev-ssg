import unittest

from generate_page import extract_title


class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        markdown = """
# Test

- This
- Is
- Nice

"""
        expected_result = "Test"
        self.assertEqual(expected_result, extract_title(markdown))

    def test_extract_title_multi_word(self):
        markdown = """
# Test Multiword

Yes, this is very nice my friend.
# What the fuck another one??

"""
        expected_result = "Test Multiword"
        self.assertEqual(expected_result, extract_title(markdown))
