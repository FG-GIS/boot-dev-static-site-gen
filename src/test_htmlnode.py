import unittest

from htmlnode import HTMLNode



class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("h1","Title")
        node2 = HTMLNode("h1","Title")
        self.assertEqual(repr(node),repr(node2))

    def test_repr_2(self):
        node = HTMLNode("a","Link",None,{"href":"https://www.boot.dev"})
        node2 = HTMLNode("a","Link",None,{"href":"https://www.boot.dev"})
        self.assertEqual(repr(node),repr(node2))
        self.assertEqual(node.props_to_html(),node2.props_to_html())
        
    def test_repr_3(self):
        node = HTMLNode("a","Link",None,{"href":"https://www.boot.dev"})
        node2 =  HTMLNode("h1","Title")
        self.assertNotEqual(repr(node),repr(node2))


if __name__ == "__main__":
    unittest.main()