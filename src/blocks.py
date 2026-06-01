from enum import Enum

from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = list(map(lambda a: a.strip(), markdown.split("\n\n")))
    full_blocks = list(filter(is_not_empty, blocks))
    return full_blocks


class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    # How to write this properly? Think about this sometimes.
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("## "):
        return BlockType.HEADING
    elif block.startswith("### "):
        return BlockType.HEADING
    elif block.startswith("#### "):
        return BlockType.HEADING
    elif block.startswith("##### "):
        return BlockType.HEADING
    elif block.startswith("###### "):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(">") and is_not_empty(line):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith("- ") and is_not_empty(line):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        lines = block.split("\n")
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def is_not_empty(x: str) -> bool:
    if x:
        return True
    else:
        return False


# This one definitely needs fine polishing, but we'll see after I finish the website generating
def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                block = block.replace("\n", " ")
                html_nodes.append(
                    ParentNode(
                        "p",
                        text_to_children(block),
                    )
                )
            case BlockType.HEADING:
                tag = md_heading_to_html_heading_tag(block)
                block = block.lstrip("# ")
                html_nodes.append(ParentNode(tag, text_to_children(block)))
            case BlockType.CODE:
                block = block.lstrip("`\n")
                block = block.rstrip("`")
                code_block = text_node_to_html_node(TextNode(block, TextType.CODE))
                html_nodes.append(ParentNode("pre", [code_block]))
            case BlockType.QUOTE:
                block = block.strip("\n").split("\n")
                quoteblock = ""
                for line in block:
                    quoteblock += line[2:] + " "
                quoteblock = quoteblock.rstrip("\n")
                html_nodes.append(
                    ParentNode("quoteblock", text_to_children(quoteblock))
                )
            case BlockType.UNORDERED_LIST:
                block = block.split("- ")
                listblock = ""
                for line in block:
                    if is_not_empty(line):
                        listblock += "<li>" + line.strip("\n") + "</li>"
                html_nodes.append(ParentNode("ul", text_to_children(listblock)))
            case BlockType.ORDERED_LIST:
                block = block.split("\n")
                listblock = ""
                for line in block:
                    if is_not_empty(line):
                        listblock += "<li>" + line[3:] + "</li>"
                html_nodes.append(ParentNode("ol", text_to_children(listblock)))

    return ParentNode("div", html_nodes)


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes


def md_heading_to_html_heading_tag(heading: str):
    level = determine_heading_level(heading)
    return f"h{level}"


def determine_heading_level(heading: str) -> int:
    if not heading.startswith("#"):
        return 0
    else:
        return 1 + determine_heading_level(heading[1:])
