import os
import shutil
import sys

from generate_page import generate_pages_recursive


def main():
    if len(sys.argv) > 0:
        basepath = sys.argv[0]
    else:
        basepath = "/"
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")
    if os.path.exists("static"):
        copy_to_docs("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


def copy_to_docs(source, destination):
    dirs = os.listdir(source)
    for item in dirs:
        full_path = os.path.join(source, item)
        if os.path.isfile(full_path):
            shutil.copy(full_path, destination)
        else:
            os.mkdir(os.path.join(destination, item))
            copy_to_docs(os.path.join(source, item), os.path.join(destination, item))


main()
