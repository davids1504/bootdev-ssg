from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        props: dict[str, str | None] | None = None,
    ):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        props = self.props_to_html()
        if not props:
            props = ""
        closing_tag = f"</{self.tag}>"
        html = f"<{self.tag}{props}>{self.value}{closing_tag}"
        return html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
