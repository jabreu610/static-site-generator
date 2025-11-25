import re

import constants


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(constants.MARKDOWN_IMAGE_CAPTURING_REGEX, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(constants.MARKDOWN_LINK_CAPTURING_REGEX, text)


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    stripped_blocks = map(lambda x: x.strip(), blocks)
    return list(filter(lambda x: len(x) > 0, stripped_blocks))


def extract_title(markdown: str):
    header_match = re.search(r"^#\s(.*)$", markdown, re.MULTILINE)
    if header_match is None:
        raise ValueError("Header not found in input")
    return header_match.group(1).strip()
