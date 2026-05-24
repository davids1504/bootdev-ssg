from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "img"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return (self.text, self.text_type, self.url) == (
            value.text,
            value.text_type,
            value.url,
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: "TextNode") -> LeafNode:

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("TextNode should have a TextType .text_type")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    text_nodes = []
    delimiters = ["`", "**", "_"]
    if delimiter not in delimiters:
        raise Exception("Unknown delimiter")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            text_nodes.append(node)
            continue
        new_nodes_texts = node.text.split(delimiter)
        if len(new_nodes_texts) % 2 == 0:
            raise Exception("Invalid Markdown syntax")
        for i, new_node_text in enumerate(new_nodes_texts):
            if new_node_text == "":
                continue
            if i % 2 == 0:
                text_nodes.append(TextNode(new_node_text, TextType.TEXT))
            else:
                text_nodes.append(TextNode(new_node_text, text_type))
    return text_nodes
