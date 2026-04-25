import re
from textnode import TextNode, TextType, text_to_textnodes
from markdownfuncs import BlockType, markdown_to_blocks, block_to_block_type

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
       self.tag = tag
       self.value = value
       self.children = children
       self.props = props

    def to_html(self):
        raise NotImplementedError("function not implemented in child class of class HTMLNode")

    def props_to_html(self):
        if not self.props:
            return ''
        formatted_props = ' '.join(f'{key}="{val}"' for key, val in self.props.items())
        return formatted_props
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.tag == "img":
            return f'<{self.tag} {self.props_to_html()}"'
        if not self.value:
            raise ValueError("all leaf nodes must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{'' if not self.props else ' ' + self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have a tag")
        if not self.children:
            raise ValueError("Parent node must have children")
        return f"<{self.tag}{'' if not self.props else ' ' + self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", '', {"src":text_node.url, "alt":text_node.text})

def markdown_to_html_node(markdown):
    #print('testing')
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        #print("-----------block start-------------")
        #print(block, "------ type = ",block_to_block_type(block))
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                html = ParentNode("p",[text_node_to_html_node(t) for t in text_to_textnodes(re.sub(r"\n", " ", block))])
            case BlockType.HEADING:
                heading_level = block.count('#')
                text = block[heading_level+1:]
                html = ParentNode(f"h{heading_level}", [text_node_to_html_node(t) for t in text_to_textnodes(text)])
            case BlockType.CODE:
                text = re.match(r"^```\n([\s\S]+)```$", block).group(1)
                html_code = ParentNode("code", [text_node_to_html_node(TextNode(text, TextType.TEXT))])
                html = ParentNode("pre", [html_code])
            case BlockType.QUOTE:
                lines = block.split("\n")
                stripped_lines = [l.lstrip(">").strip() for l in lines]
                final_lines = [l for l in stripped_lines if l != ""]
                text = " ".join(final_lines)
                html = ParentNode("blockquote", [text_node_to_html_node(t) for t in text_to_textnodes(text)])
            case BlockType.UO_LIST:
                list_items = re.findall(r"- (.+)", block)
                html = ParentNode("ul", [ParentNode("li", [text_node_to_html_node(t) for t in text_to_textnodes(i)]) for i in list_items])
            case BlockType.O_LIST:
                list_items = re.findall(r"\d\. (.+)", block)
                html = ParentNode("ol", [ParentNode("li", [text_node_to_html_node(t) for t in text_to_textnodes(i)]) for i in list_items])

        html_nodes.append(html)
        #print("------------block end-------------")

    parent_start = ParentNode("div", html_nodes)
    return parent_start
