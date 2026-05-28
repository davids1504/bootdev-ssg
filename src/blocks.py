def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = list(map(lambda a: a.strip(), markdown.split("\n\n")))
    full_blocks = list(filter(is_not_empty, blocks))
    return full_blocks


def is_not_empty(x: str) -> bool:
    if x:
        return True
    else:
        return False
