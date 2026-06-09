import os
import shutil

from generate_page import generate_page


def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    if os.path.exists("static"):
        copy_to_public("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


def copy_to_public(source, destination):
    dirs = os.listdir(source)
    for item in dirs:
        full_path = os.path.join(source, item)
        if os.path.isfile(full_path):
            shutil.copy(full_path, destination)
        else:
            os.mkdir(os.path.join(destination, item))
            copy_to_public(os.path.join(source, item), os.path.join(destination, item))


main()
