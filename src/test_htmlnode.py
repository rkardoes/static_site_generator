import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, markdown_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p", "This is a paragraph", props = {"fake":"even more fake"}) 
        node2 = HTMLNode("p", "This is a paragraph", props = {"fake":"even more fake"}) 
        node3 = HTMLNode() 
        node4 = HTMLNode() 
        node5 = HTMLNode("a", "This is a paragraph", props = {"fake":"even more fake"}) 
        node6 = HTMLNode("a", "This is a paragraph", node3, {"fake":"even more fake"}) 
        node7 = HTMLNode("a", "This is a paragraph", node4, {"fake":"even more fake"}) 
        node8 = HTMLNode("a", "This is a paragraph", node4, {"fake":"even more fake", "faker":"even more faker"})


        test_props = 'fake="even more fake" faker="even more faker"'   

        self.assertEqual(node8.props_to_html(), test_props)
        self.assertNotEqual(node7.props_to_html(), test_props)
        self.assertEqual(node6.props, node5.props)
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html(), '<a href="https://www.google.com">Click me!</a>')
        self.assertNotEqual(node, LeafNode("p", "Hello, world!", {"fake":"faker"}))

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        empty_parent_node = ParentNode("span",[])
        with self.assertRaises(ValueError):
            empty_parent_node.to_html()

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        link_node = TextNode("This is google", TextType.LINK, "www.google.com")
        link_html = text_node_to_html_node(link_node)
        self.assertEqual(link_html.props, {"href":"www.google.com"})
        self.assertEqual(link_html.to_html(), '<a href="www.google.com">This is google</a>')

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# This is a heading 1

## This is a heading 2

###### This is a heading 6

####### This is too many hashes
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading 1</h1><h2>This is a heading 2</h2><h6>This is a heading 6</h6><p>####### This is too many hashes</p></div>"
        ) 

    def test_quotes(self):
        md = """
_This_ text should be a paragraph.

> This should be a quote
> This is also a quote, but with **bold**

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p><i>This</i> text should be a paragraph.</p><blockquote>This should be a quote This is also a quote, but with <b>bold</b></blockquote><blockquote>\"I am in fact a Hobbit in all but size.\" -- J.R.R. Tolkien</blockquote></div>"
        )

    def test_unordered_lists(self):
        md = """
_This_ text should be a paragraph.

- Item
- Another _Item_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p><i>This</i> text should be a paragraph.</p><ul><li>Item</li><li>Another <i>Item</i></li></ul></div>"
        )

    def test_ordered_lists(self):
        md = """
_This_ text should be a paragraph.

1. Item
2. Another _Item_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p><i>This</i> text should be a paragraph.</p><ol><li>Item</li><li>Another <i>Item</i></li></ol></div>"
        )       

#     def test_intermediate(self):
#         md = """
# # Heading1

# ## Heading2

# This is **bolded** paragraph



# So many extra lines




# ```
# This is a code block
# ```

# 1. Ordered
# 2. List
# 3. YES

# 1. Broken
# 2. Ordered
# 5. List

# This is another paragraph with _italic_ text and `code` here
# This is the same paragraph on a new line


# This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)

# - This is a list
# - with items

# > This is a
# > Quote block
# """
#         print(markdown_to_html_node(md))


if __name__ == "__main__":
    unittest.main()
