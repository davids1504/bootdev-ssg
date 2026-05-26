import unittest

from extract_md import extract_markdown_images, extract_markdown_links


class TestMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_2(self):
        matches = extract_markdown_links(
            "My favorite search engine is [Duck Duck Go](https://duckduckgo.com)."
        )
        self.assertListEqual([("Duck Duck Go", "https://duckduckgo.com")], matches)

    def test_extract_markdown_links_2(self):
        matches = extract_markdown_links(
            "This is text with an [nice link](https://example.com), and another [even nicer link ;)](https://examplee.com)"
        )
        self.assertListEqual(
            [
                ("nice link", "https://example.com"),
                ("even nicer link ;)", "https://examplee.com"),
            ],
            matches,
        )


if __name__ == "__main__":
    unittest.main()
