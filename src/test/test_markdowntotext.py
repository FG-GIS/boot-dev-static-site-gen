import unittest

from textnode import TextNode,TextType
from converter import (split_nodes_delimiter,
                       extract_markdown_links,extract_markdown_images,
                        split_nodes_image,split_nodes_link, text_to_textnodes)
import pretty_test 



class TestMarkdownConversion(unittest.TestCase):
    def test_markdown_to_text_node_bold(self):
        node = TextNode("This is a text node, with **bold content**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        pretty_test.print_test("Markdown to Text Node", "-->This is a text node, with \n-->bold content", nodes)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0], TextNode("This is a text node, with ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("bold content", TextType.BOLD))

    def test_markdown_to_text_node_italic(self):
        node = TextNode("This is a text node, with _italic content_", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        pretty_test.print_test("Markdown to Text Node", "-->This is a text node, with \n-->italic content", nodes)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0], TextNode("This is a text node, with ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("italic content", TextType.ITALIC))
    
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
            TextNode(" after", TextType.TEXT),
        ]
        self.assertEqual(len(nodes), 2)
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

    def test_extract_markdown_links(self):
        text = "Check out [GitHub](https://github.com) and [Python](https://python.org) for more info."
        expected = [("GitHub", "https://github.com"), ("Python", "https://python.org")]
        links = extract_markdown_links(text)
        pretty_test.print_test("Markdown Links Extraction", f"Extracted links from: {text}", links)
        self.assertEqual(links, expected)

    def test_extract_markdown_links_no_links(self):
        text = "This text has no markdown links."
        expected = []
        links = extract_markdown_links(text)
        pretty_test.print_test("Markdown Links Extraction - No Links", f"Extracted links from: {text}", links)
        self.assertEqual(links, expected)

    def test_extract_markdown_links_nested_brackets(self):
        text = "Nested [Link [with] brackets](http://example.com)"
        expected = [("Link [with] brackets", "http://example.com")]
        links = extract_markdown_links(text)
        pretty_test.print_test("Markdown Links Extraction - Nested Brackets", f"Extracted links from: {text}", links)
        self.assertEqual(links, expected)

    def test_extract_markdown_images(self):
        text = "Look at this image: ![Diagram](https://example.com/diagram.png) in the documentation."
        expected = [("Diagram", "https://example.com/diagram.png")]
        images = extract_markdown_images(text)
        pretty_test.print_test("Markdown Images Extraction", f"Extracted images from: {text}", images)
        self.assertEqual(images, expected)
    
    def test_extract_markdown_images_on_link(self):
        text = "Look at this image: [Diagram](https://example.com/diagram.png) in the documentation."
        expected = [("Diagram", "https://example.com/diagram.png")]
        images = extract_markdown_images(text)
        pretty_test.print_test("Markdown Images on Links", f"Extracted images from: {text}", images)
        self.assertNotEqual(images, expected)
    
    def test_extract_markdown_link_on_image(self):
        text = "Look at this image: ![Diagram](https://example.com/diagram.png) in the documentation."
        expected = [("Diagram", "https://example.com/diagram.png")]
        images = extract_markdown_links(text)
        pretty_test.print_test("Markdown Images on Links", f"Extracted images from: {text}", images)
        self.assertNotEqual(images, expected)

    def test_extract_markdown_images_no_images(self):
        text = "There are no images in this text."
        expected = []
        images = extract_markdown_images(text)
        pretty_test.print_test("Markdown Images Extraction - No Images", f"Extracted images from: {text}", images)
        self.assertEqual(images, expected)

    def test_extract_markdown_images_malformed(self):
        # Malformed image markdown patterns that should not be extracted.
        text = "Malformed tags: ![AltText]() and ![NoURL](http://example.com without closing parenthesis"
        expected = []
        images = extract_markdown_images(text)
        pretty_test.print_test("Markdown Images Extraction - Malformed", f"Extracted images from: {text}", images)
        self.assertEqual(images, expected)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ]
        pretty_test.print_test("Split Nodes Image", expected, new_nodes)
        self.assertListEqual(expected, new_nodes)
    
    def test_split_links(self):
        # Assuming a function split_nodes_link is available,
        # which splits a text node containing a markdown link into separate nodes.
        node = TextNode("This is a test with a [link](http://example.com) included.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is a test with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(" included.", TextType.TEXT)
        ]
        pretty_test.print_test("Split Nodes Link", expected, new_nodes)
        self.assertListEqual(expected, new_nodes)

    def test_split_links_empty_input(self):
        # When provided with an empty list, split_nodes_link should return an empty list.
        new_nodes = split_nodes_link([])
        self.assertEqual(new_nodes, [])

    def test_split_links_malformed(self):
        # If the link markdown syntax is malformed, the node should remain unchanged.
        node = TextNode("Incorrect link syntax: [link(http://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_text_to_textnodes_1(self):
        # Test the full conversion of a markdown text to text nodes.
        text = "This is a **bold** and _italic_ and `code` with an ![image](https://example.com/image.png) and [link](http://example.com)."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(".", TextType.TEXT)
        ]
        pretty_test.print_test("Text to Nodes Conversion", expected, nodes)
        self.assertEqual(nodes, expected)
        
    def test_text_to_textnodes_2(self):
        # Test the full conversion of a markdown text to text nodes.
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
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
        ]
        pretty_test.print_test("Text to Nodes Conversion 2", expected, nodes)
        self.assertEqual(nodes, expected)
if __name__ == "__main__":
    unittest.main()