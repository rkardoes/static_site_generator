import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
       node1 = HTMLNode("p", "This is a paragraph", props = {"fake":"even more fake"}) 
       node2 = HTMLNode("p", "This is a paragraph", props = {"fake":"even more fake"}) 
       node3 = HTMLNode() 
       node4 = HTMLNode() 
       node5 = HTMLNode("a", "This is a paragraph", props = {"fake":"even more fake"}) 
       node6 = HTMLNode("a", "This is a paragraph", node3, {"fake":"even more fake"}) 
       node7 = HTMLNode("a", "This is a paragraph", node4, {"fake":"even more fake"}) 
       node8 = HTMLNode("a", "This is a paragraph", node4, {"fake":"even more fake"})

       self.assertEqual(node1, node2, "html 1 fail")
       self.assertNotEqual(node1, node3, "html 2 fail")
       self.assertEqual(node3, node4, "html 3 fail")
       self.assertNotEqual(node1, node5, "html 4 fail")
       self.assertNotEqual(node6, node7, "html 5 fail")
       self.assertEqual(node7, node8, "html 6 fail")

if __name__ == "__main__":
    unittest.main()