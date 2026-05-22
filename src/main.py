from textnode import TextNode, TextType

print("hello world")


def main():
    text_node = TextNode("Anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node)


main()
