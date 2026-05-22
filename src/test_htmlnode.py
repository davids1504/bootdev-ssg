import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_1(self):
        node = HTMLNode(
            "a",
            "Google",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        expected_result = ' href="https://www.google.com" target="_blank"'

        self.assertEqual(node.props_to_html(), expected_result)

    def test_props_to_html_2(self):
        node = HTMLNode(
            "img",
            None,
            None,
            {"src": "img_girl.jpg"},
        )
        expected_result = ' src="img_girl.jpg"'

        self.assertEqual(node.props_to_html(), expected_result)

    def test_props_to_html_3(self):
        node = HTMLNode(
            "img",
            None,
            None,
            {"src": "img_girl.jpg", "width": "500", "height": "600"},
        )
        expected_result = ' src="img_girl.jpg" width="500" height="600"'

        self.assertEqual(node.props_to_html(), expected_result)

    def test_props_to_html_4(self):
        node = HTMLNode(
            "p",
            "I am a paragraph without any props.",
            None,
            {},
        )
        expected_result = None

        self.assertEqual(node.props_to_html(), expected_result)


if __name__ == "__main__":
    unittest.main()
