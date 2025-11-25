import re

import constants
from block import BlockType, block_to_block_type
from extract import extract_markdown_images, extract_markdown_links, markdown_to_blocks
from htmlnode import HTMLNode, get_tag_from_block_type
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType


def text_to_leaf_nodes(text: str) -> list[HTMLNode]:
    nodes = text_to_textnodes(text)
    return list(map(text_node_to_html_node, nodes))


def get_children_for_block_type(type: BlockType, block: str) -> list[HTMLNode]:
    if type == BlockType.HEADING:
        text = re.sub(r"^#{1,6}\s+", "", block)
        return text_to_leaf_nodes(text)
    if type == BlockType.QUOTE:
        text = re.sub(r"^>\s?", "", block)
        return text_to_leaf_nodes(text)
    if type == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        return list(
            map(
                lambda x: ParentNode("li", text_to_leaf_nodes(re.sub(r"^-\s+", "", x))),
                lines,
            )
        )
    if type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        return list(
            map(
                lambda x: ParentNode(
                    "li", text_to_leaf_nodes(re.sub(r"^\d+\.\s+", "", x))
                ),
                lines,
            )
        )
    if type == BlockType.CODE:
        return [
            text_node_to_html_node(
                TextNode("".join(block.splitlines(True)[1:-1]), TextType.CODE)
            )
        ]
    return text_to_leaf_nodes(block.strip().replace("\n", " "))


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    html_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        tag = get_tag_from_block_type(block_type, block)
        children = get_children_for_block_type(block_type, block)
        html_children.append(ParentNode(tag, children))
    return ParentNode("div", html_children)


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.url:
                return LeafNode("a", text_node.text, {"href": text_node.url})
            raise ValueError("Text nodes of type 'LINK' must include a URL")
        case TextType.IMAGE:
            return LeafNode(
                "img", "", {"src": text_node.url or "", "alt": text_node.text}
            )


def split_nodes_delimiter(
    nodes_to_transform: list[TextNode], delimiter: str, text_type: TextType
):
    output: list[TextNode] = []
    for node in nodes_to_transform:
        if node.text_type != TextType.PLAIN:
            output.append(node)
            continue
        segments = node.text.split(delimiter)
        if len(segments) % 2 == 0:
            raise ValueError("Input text node should include pairs of delimiter")
        for index in range(len(segments)):
            if len(segments[index]) == 0:
                continue
            if (index + 1) % 2 != 0:
                output.append(TextNode(segments[index], TextType.PLAIN))
            else:
                output.append(TextNode(segments[index], text_type))
    return output


def split_nodes_image(nodes_to_transform: list[TextNode]) -> list[TextNode]:
    output = []
    for node in nodes_to_transform:
        if node.text_type != TextType.PLAIN:
            output.append(node)
            continue
        segments = re.split(constants.MARKDOWN_IMAGE_REGEX, node.text)
        for segment in segments:
            if len(segment) == 0:
                continue
            if re.fullmatch(constants.MARKDOWN_IMAGE_REGEX, segment) is None:
                output.append(TextNode(segment, TextType.PLAIN))
                continue
            images = extract_markdown_images(segment)
            for alt, image in images:
                output.append(TextNode(alt, TextType.IMAGE, image))
    return output


def split_nodes_link(nodes_to_transform: list[TextNode]) -> list[TextNode]:
    output = []
    for node in nodes_to_transform:
        if node.text_type != TextType.PLAIN:
            output.append(node)
            continue
        segments = re.split(constants.MARKDOWN_LINK_REGEX, node.text)
        for segment in segments:
            if len(segment) == 0:
                continue
            if re.fullmatch(constants.MARKDOWN_LINK_REGEX, segment) is None:
                output.append(TextNode(segment, TextType.PLAIN))
                continue
            links = extract_markdown_links(segment)
            for text, url in links:
                output.append(TextNode(text, TextType.LINK, url))
    return output


def text_to_textnodes(text: str):
    root_node = TextNode(text, TextType.PLAIN)
    with_bold = split_nodes_delimiter([root_node], "**", TextType.BOLD)
    with_italics = split_nodes_delimiter(with_bold, "_", TextType.ITALIC)
    with_code = split_nodes_delimiter(with_italics, "`", TextType.CODE)
    with_images = split_nodes_image(with_code)
    return split_nodes_link(with_images)
