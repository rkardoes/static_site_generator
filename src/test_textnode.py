import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


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
        node6 = TextNode("This is a text with bold at the **end**", TextType.TEXT)
        new_nodes6 = split_nodes_delimiter([node6], "**", TextType.BOLD)
        expected6 = [
                    TextNode("This is a text with bold at the ", TextType.TEXT),
                    TextNode("end", TextType.BOLD),
                    ]
        self.assertEqual(new_nodes6, expected6)
        node7 = TextNode("**This** is a text with bold at the beginning", TextType.TEXT)
        new_nodes7 = split_nodes_delimiter([node7], "**", TextType.BOLD)
        expected7 = [
                    TextNode("This", TextType.BOLD),
                    TextNode(" is a text with bold at the beginning", TextType.TEXT),
                    ]
        self.assertEqual(new_nodes7, expected7)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and some text after it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and some text after it", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with an [link](www.google.com) and another [second link](www.bing.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "www.bing.com"
                ),
            ],
            new_nodes,
        )
        node = TextNode(
            "This is text with an [link](www.google.com)[second link](www.bing.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.google.com"),
                TextNode(
                    "second link", TextType.LINK, "www.bing.com"
                ),
            ],
            new_nodes,
        )
        node = TextNode(
            "This is text with an [](www.google.com)[second link](www.bing.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("", TextType.LINK, "www.google.com"),
                TextNode(
                    "second link", TextType.LINK, "www.bing.com"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ], 
            text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
         )

if __name__ == "__main__":
    unittest.main()