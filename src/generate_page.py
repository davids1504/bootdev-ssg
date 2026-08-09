import os
import shutil

from blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path, basepath):
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
    ).replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")
    if os.path.dirname(dest_path) != "":
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(html_page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dirs = os.listdir(dir_path_content)
    for item in dirs:
        full_path = os.path.join(dir_path_content, item)
        if os.path.isfile(full_path) and item.endswith('.md'):
            generate_page(full_path, template_path, os.path.join(dest_dir_path, os.path.splitext(item)[0] + ".html"), basepath)
        else:
            if not os.path.isfile(full_path):
                if os.path.dirname(os.path.join(dest_dir_path, item)):
                    os.makedirs(os.path.join(dest_dir_path, item), exist_ok=True)
                generate_pages_recursive(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, item), basepath)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 found in the markdown file")
