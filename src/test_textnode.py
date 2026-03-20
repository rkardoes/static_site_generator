import unittest

from textnode import TextNode, TextType, split_nodes_delimiter


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

    def test_split_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.TEXT),
                    ]
        self.assertEqual(new_nodes, expected)
        node2 = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], "_", TextType.ITALIC)
        expected2 = [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word", TextType.TEXT),
                    ]
        self.assertEqual(new_nodes2, expected2)
        node3 = TextNode("This is text with a _italic_ word and a **bold** word", TextType.TEXT)
        new_nodes3 = split_nodes_delimiter([node3], "_", TextType.ITALIC)
        expected3 = [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a **bold** word", TextType.TEXT),
                    ]
        self.assertEqual(new_nodes3, expected3)
        new_nodes4 = split_nodes_delimiter(new_nodes3, "**", TextType.BOLD)
        expected4 = [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" word", TextType.TEXT),
                    ]
        self.assertEqual(new_nodes4, expected4)
        node5 = TextNode("This is text with a _italic word and a **bold** word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node5], "_", TextType.ITALIC)

if __name__ == "__main__":
    unittest.main()