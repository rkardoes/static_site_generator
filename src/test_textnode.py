import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.LINK, "google.com")
        node5 = TextNode("This is a text node", TextType.LINK, "google.come")
        node6 = TextNode("This is a text node", TextType.IMAGE, "image.jpg")
        node7 = TextNode("This is a text node", TextType.IMAGE)
        node8 = TextNode("This is a text node", TextType.IMAGE)
        node9 = TextNode("This is a text node", TextType.LINK, "google.com")
        self.assertEqual(node, node2)
        self.assertNotEqual(node3, node2)
        self.assertNotEqual(node4, node5)
        self.assertNotEqual(node6, node7)
        self.assertEqual(node7, node8)
        self.assertEqual(node4, node9)


if __name__ == "__main__":
    unittest.main()