import re

import constants


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(constants.MARKDOWN_IMAGE_CAPTURING_REGEX, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(constants.MARKDOWN_LINK_CAPTURING_REGEX, text)


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    return list(map(lambda x: x.strip(), filter(lambda x: len(x) > 0, blocks)))
