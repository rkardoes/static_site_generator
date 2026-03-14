from textnode import TextNode, TextType


def main():
    test_node_text = TextNode("This is a text test", TextType.text)
    test_node_bold = TextNode("This is a bold test.", TextType.bold)
    test_node_italic = TextNode("This is an italic test", TextType.italic)
    test_node_code = TextNode("This is a code node.", TextType.code)
    test_node_link = TextNode("This is a link.", TextType.link, "www.google.com")
    test_node_image = TextNode("This is an image with no URL.", TextType.image)

    print(test_node_link)

main()