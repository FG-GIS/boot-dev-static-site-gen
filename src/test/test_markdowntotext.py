import unittest

from textnode import TextNode,TextType
from converter import split_nodes_delimiter
import pretty_test 



class TestMarkdownConversion(unittest.TestCase):
    def test_markdown_to_text_node_bold(self):
        node = TextNode("This is a text node, with **bold content**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        pretty_test.print_test("Markdown to Text Node", "-->This is a text node, with \n-->bold content\n-->", nodes)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0], TextNode("This is a text node, with ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("bold content", TextType.BOLD))
        self.assertEqual(nodes[2], TextNode("", TextType.TEXT))

    def test_markdown_to_text_node_italic(self):
        node = TextNode("This is a text node, with _italic content_", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        pretty_test.print_test("Markdown to Text Node", "-->This is a text node, with \n-->italic content\n-->", nodes)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0], TextNode("This is a text node, with ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("italic content", TextType.ITALIC))
        self.assertEqual(nodes[2], TextNode("", TextType.TEXT))
    
    def test_markdown_to_text_node_code(self):
        node = TextNode("This is a text node, with `code snippet` example", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        pretty_test.print_test("Markdown to Text Node", "-->This is a text node, with \n-->code snippet\n--> example", nodes)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0], TextNode("This is a text node, with ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("code snippet", TextType.CODE))
        self.assertEqual(nodes[2], TextNode(" example", TextType.TEXT))
    
    def test_markdown_no_delimiter(self):
        node = TextNode("This text has no delimiters", TextType.TEXT)
        # Since the delimiter is not found, the original node should be returned unchanged.
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], node)

    def test_markdown_multiple_bold_occurrences(self):
        node = TextNode("Start **first bold** middle **second bold** end", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("first bold", TextType.BOLD),
            TextNode(" middle ", TextType.TEXT),
            TextNode("second bold", TextType.BOLD),
            TextNode(" end", TextType.TEXT)
        ]
        self.assertEqual(len(nodes), 5)
        for n, exp in zip(nodes, expected):
            self.assertEqual(n, exp)

    def test_markdown_empty_bold(self):
        node = TextNode("Before **** after", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("", TextType.BOLD),
            TextNode(" after", TextType.TEXT)
        ]
        self.assertEqual(len(nodes), 3)
        for n, exp in zip(nodes, expected):
            self.assertEqual(n, exp)

    def test_markdown_empty_input_list(self):
        # When provided with an empty list, the function should return an empty list.
        nodes = split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertEqual(nodes, [])

    def test_multiple_delimiters(self):
        # Test multiple applications of split_nodes_delimiter using different delimiters.
        # First apply italic conversion then bold conversion on text nodes.
        node = TextNode("Combine _italic_ and **bold** effects", TextType.TEXT)
        # Split by italic delimiter "_"
        intermediate_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        final_nodes = []
        for n in intermediate_nodes:
            if n.text_type == TextType.TEXT:
                # Split by bold delimiter "**" on TEXT nodes
                bold_nodes = split_nodes_delimiter([n], "**", TextType.BOLD)
                final_nodes.extend(bold_nodes)
            else:
                final_nodes.append(n)
        expected = [
            TextNode("Combine ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" effects", TextType.TEXT)
        ]
        self.assertEqual(final_nodes, expected)

if __name__ == "__main__":
    unittest.main()