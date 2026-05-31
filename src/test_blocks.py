import unittest

from blocks import BlockType, block_to_block_type, markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()
