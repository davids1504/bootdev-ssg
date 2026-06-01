import unittest

from blocks import (
    BlockType,
    block_to_block_type,
    determine_heading_level,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_spaces(self):
        md = """
This is **bolded** paragraph






This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line







- This is a list
- with items
- a
- b
- i
- g
- f
- k
- l
- i
- s
- t
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items\n- a\n- b\n- i\n- g\n- f\n- k\n- l\n- i\n- s\n- t",
            ],
        )

    def test_b2b_heading(self):
        block = "# Hello"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_b2b_code(self):
        block = """```
void main() {
    print("Hello, Dart")
    print("Assert me, Daddy")
}
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_b2b_quote(self):
        block = ">Hello\n> World"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_b2b_ul(self):
        block = """- It's my world, and
- You can't have it
- It's my world, and
- You can't have it"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_b2b_ol(self):
        block = """1. Take a wrench
2. Build a car
3. Drink beer
4. Crash you wrench
5. Drink a refreshing engine beverage"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_b2b_ul_false(self):
        block = """- It's my world, and
- You can't have it
- It's my world, and
-You can't have it"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_b2b_ol_false(self):
        block = """1. Take a wrench
2. Build a car
3. Drink beer
4. Crash you wrench
6. Drink a refreshing engine beverage"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_b2b_code_false(self):
        block = """```
void main() {
    print("Hello, Dart")
    print("Assert me, Daddy")
}
``"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_paragraphs_and_headings(self):
        md = """
# Main heading

This is **bolded** paragraph
text in a p
tag here

## Heading 2

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main heading</h1><p>This is <b>bolded</b> paragraph text in a p tag here</p><h2>Heading 2</h2><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
> This is text that _should_ remain
> the **same** even with inline stuff
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><quoteblock>This is text that <i>should</i> remain the <b>same</b> even with inline stuff </quoteblock></div>",
        )

    def test_ul(self):
        md = """- First
- Second"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<div><ul><li>First</li><li>Second</li></ul></div>",
        )

    def test_ol(self):
        md = """1. First
2. Second"""

        node = markdown_to_html_node(md.strip("\n"))
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li></ol></div>",
        )

    def test_heading_level_1(self):
        heading = "# Head"
        self.assertEqual(determine_heading_level(heading), 1)

    def test_heading_level_3(self):
        heading = "### Head"
        self.assertEqual(determine_heading_level(heading), 3)

    def test_heading_level_6(self):
        heading = "###### Head"
        self.assertEqual(determine_heading_level(heading), 6)

    def test_heading_level_0(self):
        heading = "Head"
        self.assertEqual(determine_heading_level(heading), 0)


if __name__ == "__main__":
    unittest.main()
