import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph block",
    HEADING = "heading block"
    CODE = "code block"
    QUOTE = "quote block"
    UO_LIST = "unordered list block"
    O_LIST = "ordered list block"

def extract_markdown_images(text):
    images = re.findall(r"!\[(.*?)]\((.*?)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"\[(.*?)]\((.*?)\)", text)
    return links

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [b.strip() for b in blocks if b.strip() != ""]
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")
    heading = re.match(r"^#{1,6} ", lines[0]) and len(lines) == 1
    code = re.match(r"^```\n[\s\S]*\n```$", block)
    quote = all([re.match(r"^>", l) for l in lines])
    unordered = all([re.match(r"^- ", l) for l in lines])
    ordered = all([re.match(f"{i+1}. ", l) for i, l in enumerate(lines)])

    if heading:
        return BlockType.HEADING
    if code:
        return BlockType.CODE
    if quote:
        return BlockType.QUOTE
    if unordered:
        return BlockType.UO_LIST
    if ordered:
        return BlockType.O_LIST
    return BlockType.PARAGRAPH

def extract_title(markdown):
    title = re.search(r"# ([\S\s]+?)\n", markdown)
    if title is not None:
        return title.group(1)
    raise Exception("no title")