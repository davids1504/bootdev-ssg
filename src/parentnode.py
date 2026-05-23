from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        children: list[HTMLNode] | None,
        props: dict[str, str | None] | None = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a defined tag parameter")
        if self.children is None:
            raise ValueError("ParentNode must have a defined children parameter")

        html: str = ""
        for childNode in self.children:
            html += childNode.to_html()
        html = f"<{self.tag}>{html}</{self.tag}>"
        return html

    def __repr__(self):
        return f"Parentnode({self.tag}, children: {self.children}, {self.props})"
