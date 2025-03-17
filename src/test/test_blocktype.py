import unittest

from blocktype import *



class TestBlocktoBlockType(unittest.TestCase):
    def test_block_to_block_type_base(self):
        blocks = ["### This is **Header** block",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "```this is a code block```"]
        
        block_tpyes = [BlockType.HEADING,BlockType.PARAGRAPH,BlockType.UNORDERED_LIST,BlockType.CODE,]

        self.assertEqual(list(map(block_to_block_type,blocks)),block_tpyes)

    def test_block_to_block_type_ordered_list(self):
        blocks = ["1. This is a list\n\
2. with 2 elements","this is a paraggraph"]
        block_tpyes = [BlockType.ORDERED_LIST,BlockType.PARAGRAPH]
        out = list(map(block_to_block_type,blocks))
        # print("comparing:",blocks)
        # print("to: ",out)
        self.assertEqual(out,block_tpyes)
                

    def test_block_to_block_type_quote(self):
        blocks = [
            "> This is a quote\n> Second line of quote",
            "> Single line quote",
            "Not a > quote"
        ]
        block_types = [
            BlockType.QUOTE,
            BlockType.QUOTE, 
            BlockType.PARAGRAPH
        ]
        self.assertEqual(list(map(block_to_block_type, blocks)), block_types)

    def test_block_to_block_type_heading_levels(self):
        blocks = [
            "# H1 Heading",
            "## H2 Heading",
            "### H3 Heading", 
            "#### H4 Heading",
            "##### H5 Heading",
            "###### H6 Heading",
            "#Not a heading",
            "####### Invalid heading"
        ]
        block_types = [
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING, 
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH
        ]
        self.assertEqual(list(map(block_to_block_type, blocks)), block_types)

    def test_block_to_block_type_complex_ordered_list(self):
        blocks = [
            "1. First item\n2. Second item\n3. Third item",
            "1. First\n2. Second\n4. Invalid sequence", 
            "0. Invalid start\n1. Second item",
            "1. Single item"
        ]
        block_types = [
            BlockType.ORDERED_LIST,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.ORDERED_LIST
        ]
        self.assertEqual(list(map(block_to_block_type, blocks)), block_types)

if __name__ == '__main__':
    unittest.main()