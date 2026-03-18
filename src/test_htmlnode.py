import unittest

from htmlnode import HTMLNode, LeafNode

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
        

if __name__ == "__main__":
    unittest.main()
