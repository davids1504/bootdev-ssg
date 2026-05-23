import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode(
            "a",
            "Click me!",
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">Click me!</a>',
        )

    def test_leaf_to_html_b(self):
        node = LeafNode(
            "b",
            "I want to emphasise this!",
            {"color": "green", "class": "super-bold"},
        )
        self.assertEqual(
            node.to_html(),
            '<b color="green" class="super-bold">I want to emphasise this!</b>',
        )

    def test_leaf_to_html_i(self):
        node = LeafNode(
            "i",
            "Curvy text is curvy.",
            {"color": "blue", "class": "super-bold"},
        )
        self.assertEqual(
            node.to_html(),
            '<i color="blue" class="super-bold">Curvy text is curvy.</i>',
        )


if __name__ == "__main__":
    unittest.main()
