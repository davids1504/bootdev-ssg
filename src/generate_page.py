import os

from blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    template = ""
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    html_page = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_node
    )
    if os.path.dirname(dest_path) != "":
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(html_page)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 found in the markdown file")
