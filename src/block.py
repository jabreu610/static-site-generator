import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if re.fullmatch(r"^#{1,6} .*$", block) is not None:
        return BlockType.HEADING
    elif re.fullmatch(r"^`{3}\n?(?:.+\n?)+`{3}$", block, re.M) is not None:
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif re.fullmatch(r"^(?:-\s.+\n?)+$", block, re.M) is not None:
        return BlockType.UNORDERED_LIST
    elif re.fullmatch(r"^(?:\d+\.\s.+\n?)+$", block, re.M) is not None:
        current_digit: int | None = None
        is_valid = True
        for line in block.split("\n"):
            num = int(line[: line.find(".")])
            if isinstance(current_digit, int):
                if num == current_digit + 1:
                    current_digit = num
                else:
                    is_valid = False
                    break
            else:
                current_digit = num
        if is_valid:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
