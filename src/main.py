import os
import shutil

from textnode import TextNode, TextType

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


def main():
    initialize_public()


main()
