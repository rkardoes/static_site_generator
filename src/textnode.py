from enum import Enum
from markdownfuncs import extract_markdown_links, extract_markdown_images

class TextType(Enum):
    TEXT = "plain text" 
    BOLD = "bold text" 
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text 
                and self.text_type == other.text_type 
                and self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            # max len(splits) = 3, if len(splits) = 2 raise error 
            splits = node.text.split(delimiter, 2)
            if len(splits) == 2:
                raise Exception("Invalid markdown, missing closing delimiter")
            elif len(splits) == 1:
                new_nodes.append(node)
            else:
                beg = TextNode(splits[0], TextType.TEXT)
                mid = TextNode(splits[1], text_type=text_type)
                end = TextNode(splits[2], TextType.TEXT)
                if beg.text != "":
                    new_nodes.append(beg)
                new_nodes.append(mid)
                if end.text != "":
                    new_nodes.extend(split_nodes_delimiter([end], delimiter=delimiter, text_type=text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text
            imgs = extract_markdown_images(text)
            for img in imgs:
                splits = text.split(f"![{img[0]}]({img[1]})", 1)
                before = TextNode(splits[0], TextType.TEXT)
                im = TextNode(img[0], TextType.IMAGE, img[1])
                if before.text != '':
                    new_nodes.append(before)
                new_nodes.append(im)
                text = splits[1]
            if text != '':
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text
            links = extract_markdown_links(text)
            for link in links:
                splits = text.split(f"[{link[0]}]({link[1]})", 1)
                before = TextNode(splits[0], TextType.TEXT)
                lin = TextNode(link[0], TextType.LINK, link[1])
                if before.text != '':
                    new_nodes.append(before)
                new_nodes.append(lin)
                text = splits[1]
            if text != '':
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    return nodes
