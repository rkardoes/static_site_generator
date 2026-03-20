from textnode import TextNode, TextType


def main():
    test_node_text = TextNode("This is a text test", TextType.TEXT)
    test_node_bold = TextNode("This is a bold test.", TextType.BOLD)
    test_node_italic = TextNode("This is an italic test", TextType.ITALIC)
    test_node_code = TextNode("This is a code node.", TextType.CODE)
    test_node_link = TextNode("This is a link.", TextType.LINK, "www.google.com")
    test_node_image = TextNode("This is an image with no URL.", TextType.IMAGE)

    print(test_node_link)

main()