import os
import shutil
from pathlib import Path

from extract import extract_title
from transform import markdown_to_html_node

DEST = "./public"
SRC = "./static"


def initialize_public(path=""):
    global DEST, SRC
    destination = os.path.join(DEST, path)
    source = os.path.join(SRC, path)
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    for entry in os.listdir(source):
        to_copy = os.path.join(source, entry)
        if os.path.isdir(to_copy):
            initialize_public(os.path.join(path, entry))
        else:
            shutil.copy(
                to_copy,
                destination,
            )


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = read_file_to_string(from_path)
    template = read_file_to_string(template_path)
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    out = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    dest = Path(dest_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    with os.scandir(dir_path_content) as entries:
        for entry in entries:
            src = os.path.join(dir_path_content, entry.name)
            if entry.is_file() and entry.name.endswith(".md"):
                generate_page(
                    src,
                    template_path,
                    os.path.join(dest_dir_path, entry.name.replace(".md", ".html")),
                )
            elif entry.is_dir():
                generate_pages_recursive(
                    src, template_path, os.path.join(dest_dir_path, entry.name)
                )


def read_file_to_string(path):
    out = None
    with open(path, "r") as file:
        out = file.read()
    return out


def main():
    initialize_public()
    generate_pages_recursive("content", "template.html", "public")


main()
