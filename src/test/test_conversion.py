import unittest

from textnode import TextNode,TextType
from converter import text_node_to_html_node,markdown_to_blocks
import pretty_test
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode


class TestConversions(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        pretty_test.print_test("conversion test 1", "This is a text node", html_node.value)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        pretty_test.print_test("conversion test 2", "Bold text", html_node.value)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        pretty_test.print_test("conversion test 3", "Italic text", html_node.value)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        pretty_test.print_test("conversion test 4", "print('Hello')", html_node.value)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")

    def test_link(self):
        node = TextNode("GitHub", TextType.LINK)
        node.url = "https://github.com"
        html_node = text_node_to_html_node(node)
        pretty_test.print_test("conversion test 5", "GitHub", html_node.value)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "GitHub")
        self.assertIn("href", html_node.props)
        self.assertEqual(html_node.props["href"], "https://github.com")

    def test_image(self):
        node = TextNode("Image alt", TextType.IMAGE)
        node.url = "https://example.com/image.png"
        html_node = text_node_to_html_node(node)
        pretty_test.print_test("conversion test 6", "", html_node.to_html())
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertIn("src", html_node.props)
        self.assertEqual(html_node.props["src"], "https://example.com/image.png")
        self.assertIn("alt", html_node.props)
        self.assertEqual(html_node.props["alt"], "Image alt")

    def test_unknown_text_type_raises(self):
        # Using an undefined text type should raise ValueError.
        node = TextNode("Unknown", "UNKNOWN")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

class TestConversionHierarchy(unittest.TestCase):
    def test_nested_conversion(self):
        # Convert individual text nodes and nest them inside a parent element.
        italic = text_node_to_html_node(TextNode("Italic text", TextType.ITALIC))
        bold = text_node_to_html_node(TextNode("Bold text", TextType.BOLD))
        # Wrap the converted nodes in a paragraph.
        parent = ParentNode("p", [italic, bold])
        expected = "<p><i>Italic text</i><b>Bold text</b></p>"
        pretty_test.print_test("hierarchy test 1", expected, parent.to_html())
        self.assertEqual(parent.to_html(), expected)

    def test_conversion_with_props_in_hierarchy(self):
        # Convert a text node and wrap it in a parent node that has properties.
        text_conv = text_node_to_html_node(TextNode("Child text", TextType.TEXT))
        parent = ParentNode("section", [text_conv], props={"class": "content", "id": "main"})
        expected_props = ' class="content" id="main"'
        # For TEXT conversion, LeafNode tag is None so the output is just the value.
        expected = f"<section{expected_props}>Child text</section>"
        pretty_test.print_test("hierarchy test 2", expected, parent.to_html())
        self.assertEqual(parent.to_html(), expected)

    def test_multiple_nested_levels(self):
        # Create a nested hierarchy: div > article > p with mixed converted text nodes.
        text1 = text_node_to_html_node(TextNode("First paragraph.", TextType.TEXT))
        p = ParentNode("p", [text1])
        article = ParentNode("article", [p])
        div = ParentNode("div", [article], props={"class": "wrapper"})
        expected_props = ' class="wrapper"'
        expected = f"<div{expected_props}><article><p>First paragraph.</p></article></div>"
        pretty_test.print_test("hierarchy test 3", expected, div.to_html())
        self.assertEqual(div.to_html(), expected)

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

if __name__ == '__main__':
    unittest.main()

