from enum import Enum

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
                new_nodes.extend([beg, mid])
                new_nodes.extend(split_nodes_delimiter([end], delimiter=delimiter, text_type=text_type))
    return new_nodes