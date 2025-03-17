from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(txt_block: str) -> BlockType:
    if re.match(r"^\#{1,6}? .*?",txt_block):
        return BlockType.HEADING
    if re.match(r"(?m)^`{3}\n?|\n?`{3}$",txt_block):
        return BlockType.CODE
    if re.match(r"(?m)^> .*?",txt_block):
        return BlockType.QUOTE
    if re.match(r"(?m)^- .*?",txt_block):
        return BlockType.UNORDERED_LIST
    flag = True
    lines = txt_block.split("\n")
    n_lines = len(lines)
    for i in range(n_lines):
        n = 0
        n_str = re.match(r"^(\d+)\. ",lines[i])
        if n_str:
            n = int(n_str.group(1))
        if n != i+1:
            flag = False
    if flag:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


