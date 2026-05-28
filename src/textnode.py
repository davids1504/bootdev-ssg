from enum import Enum

from extract_md import extract_markdown_images, extract_markdown_links
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


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    text_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            text_nodes.append(node)
            continue
        link_nodes = extract_markdown_links(node.text)
        if len(link_nodes) == 0:
            text_nodes.append(node)
            continue
        current_section = node.text
        for i in range(len(link_nodes)):
            link_text = link_nodes[i][0]
            link_href = link_nodes[i][1]
            sections = current_section.split(f"[{link_text}]({link_href})", 1)
            if sections[0] != "":
                text_nodes.append(TextNode(sections[0], TextType.TEXT))
            text_nodes.append(TextNode(link_text, TextType.LINK, link_href))

            current_section = sections[1]
        if current_section != "":
            text_nodes.append(TextNode(current_section, TextType.TEXT))

    return text_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    text_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            text_nodes.append(node)
            continue
        image_nodes = extract_markdown_images(node.text)
        if len(image_nodes) == 0:
            text_nodes.append(node)
            continue
        current_section = node.text
        for i in range(len(image_nodes)):
            image_alt = image_nodes[i][0]
            image_url = image_nodes[i][1]
            sections = current_section.split(f"![{image_alt}]({image_url})", 1)
            if sections[0] != "":
                text_nodes.append(TextNode(sections[0], TextType.TEXT))
            text_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

            current_section = sections[1]
        if current_section != "":
            text_nodes.append(TextNode(current_section, TextType.TEXT))

    return text_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes = [TextNode(text, TextType.TEXT)]
    splitted = split_nodes_delimiter(
        split_nodes_delimiter(
            split_nodes_delimiter(text_nodes, "**", TextType.BOLD), "`", TextType.CODE
        ),
        "_",
        TextType.ITALIC,
    )
    return split_nodes_link(split_nodes_image(splitted))
