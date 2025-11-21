from __future__ import annotations

import re

from block import BlockType


def get_tag_from_block_type(block_type: BlockType, block: str) -> str:
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            prefix = re.match("^#{1,6}", block)
            if prefix:
                level = len(prefix.group(0))
                return f"h{level}"
            # fallback is level cannot be determined
            return "h1"
        case BlockType.CODE:
            return "pre"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        obj = self.props
        output_list = map(lambda x: f'{x}="{obj[x]}"', obj)
        return f" {' '.join(output_list)} "

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
