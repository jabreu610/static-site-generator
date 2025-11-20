from leafnode import LeafNode
from textnode import TextNode, TextType


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
            return LeafNode("img", "", {"src": "", "alt": ""})


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
