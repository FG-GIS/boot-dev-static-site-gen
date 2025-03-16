import unittest

from htmlnode import ParentNode,LeafNode
import pretty_test



class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        expected = "<div><span>child</span></div>"
        pretty_test.print_test(self.test_to_html_with_children,expected,parent_node.to_html())
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        expected = "<div><span><b>grandchild</b></span></div>"
        pretty_test.print_test(self.test_to_html_with_grandchildren,expected,parent_node.to_html())
        self.assertEqual(
            parent_node.to_html(),
            expected,
        )

        # New edge case tests begin here:
    def test_empty_tag_raises(self):
        # A parent node with an empty tag should raise a ValueError.
        child_node = LeafNode("span", "child")
        with self.assertRaises(ValueError):
            ParentNode("", [child_node]).to_html()

    def test_none_tag_raises(self):
        # A parent node with tag set to None should raise a ValueError.
        child_node = LeafNode("span", "child")
        with self.assertRaises(ValueError):
            ParentNode(None, [child_node]).to_html()

    def test_no_children_raises(self):
        # A parent node with an empty children list should raise a ValueError.
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_props_handling(self):
        # A parent node with properties should include the props in the output.
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], props={"class": "container", "id": "main"})
        expected_props = ' class="container" id="main"'
        expected_html = f"<div{expected_props}><span>child</span></div>"
        pretty_test.print_test(self.test_props_handling,expected_html,parent_node.to_html())
        self.assertEqual(parent_node.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()