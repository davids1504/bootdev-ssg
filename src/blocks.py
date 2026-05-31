from enum import Enum


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = list(map(lambda a: a.strip(), markdown.split("\n\n")))
    full_blocks = list(filter(is_not_empty, blocks))
    return full_blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if block.startswith("# "):
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
