import unittest

from block import BlockType, block_to_block_type


class TestBlock(unittest.TestCase):
    def test_block_to_block_type_heading_h1(self):
        block = "# This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, result)

    def test_block_to_block_type_heading_h2(self):
        block = "## This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, result)

    def test_block_to_block_type_heading_h6(self):
        block = "###### This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, result)

    def test_block_to_block_type_heading_invalid_no_space(self):
        # Heading without space after # should be paragraph
        block = "#This is not a heading"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_heading_invalid_too_many_hashes(self):
        # More than 6 hashes should be paragraph
        block = "####### This is not a heading"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_code(self):
        block = "```\ncode here\n```"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, result)

    def test_block_to_block_type_code_multiline(self):
        block = "```\nline 1\nline 2\nline 3\n```"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, result)

    def test_block_to_block_type_quote_single_line(self):
        block = "> This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, result)

    def test_block_to_block_type_quote_multiline(self):
        block = "> This is a quote\n> with multiple lines"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, result)

    def test_block_to_block_type_unordered_list_dash(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, result)

    def test_block_to_block_type_unordered_list_single_item(self):
        block = "- Single item"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, result)

    def test_block_to_block_type_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, result)

    def test_block_to_block_type_ordered_list_single_item(self):
        block = "1. Single item"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, result)

    def test_block_to_block_type_ordered_list_invalid_sequence(self):
        # Non-sequential numbers should be paragraph
        block = "1. First item\n3. Third item\n2. Second item"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_ordered_list_skip_number(self):
        # Skipping numbers should be paragraph
        block = "1. First item\n2. Second item\n4. Fourth item"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_paragraph(self):
        block = "This is just a regular paragraph."
        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_paragraph_multiline(self):
        block = "This is a paragraph\nwith multiple lines\nbut no special formatting."
        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_paragraph_with_bold(self):
        block = "This is a paragraph with **bold** text."
        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_empty_string(self):
        # Empty string should be paragraph
        block = ""
        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result)


if __name__ == "__main__":
    unittest.main()
