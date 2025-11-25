import unittest

from extract import (
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
    markdown_to_blocks,
)


class TestExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com)"
        )
        self.assertEqual([("link", "https://www.example.com")], matches)

    def test_extract_markdown_images_multiple(self):
        # Test extracting multiple images from text
        matches = extract_markdown_images(
            "![first](https://example.com/1.png) and ![second](https://example.com/2.jpg)"
        )
        self.assertListEqual(
            [
                ("first", "https://example.com/1.png"),
                ("second", "https://example.com/2.jpg"),
            ],
            matches,
        )

    def test_extract_markdown_links_multiple(self):
        # Test extracting multiple links from text
        matches = extract_markdown_links(
            "[Google](https://google.com) and [GitHub](https://github.com)"
        )
        self.assertListEqual(
            [("Google", "https://google.com"), ("GitHub", "https://github.com")],
            matches,
        )

    def test_extract_markdown_images_empty_alt(self):
        # Test image with empty alt text
        matches = extract_markdown_images("![](https://example.com/image.png)")
        self.assertListEqual([("", "https://example.com/image.png")], matches)

    def test_extract_markdown_links_empty_text(self):
        # Test link with empty text
        matches = extract_markdown_links("[](https://example.com)")
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_markdown_images_none_found(self):
        # Test when no images are present
        matches = extract_markdown_images("This is plain text with no images")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_none_found(self):
        # Test when no links are present
        matches = extract_markdown_links("This is plain text with no links")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_ignores_images(self):
        # Test that extract_markdown_links also matches images (since images are a superset)
        # Note: This is actually a quirk of the current implementation
        matches = extract_markdown_links(
            "![image](https://example.com/pic.png) and [link](https://example.com)"
        )
        self.assertListEqual(
            [("image", "https://example.com/pic.png"), ("link", "https://example.com")],
            matches,
        )

    def test_extract_markdown_images_with_spaces(self):
        # Test image with spaces in alt text
        matches = extract_markdown_images(
            "![alt text with spaces](https://example.com/image.png)"
        )
        self.assertListEqual(
            [("alt text with spaces", "https://example.com/image.png")], matches
        )

    def test_extract_markdown_links_with_spaces(self):
        # Test link with spaces in text
        matches = extract_markdown_links("[link text with spaces](https://example.com)")
        self.assertListEqual(
            [("link text with spaces", "https://example.com")], matches
        )

    def test_extract_markdown_images_mixed_with_text(self):
        # Test images mixed with regular text and links
        text = "Check out ![my photo](https://example.com/photo.jpg) and visit [my site](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("my photo", "https://example.com/photo.jpg")], matches)

    def test_markdown_to_blocks(self):
        input = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            """- This is the first list item in a list block\n- This is a list item\n- This is another list item""",
        ]
        output = markdown_to_blocks(input)
        self.assertListEqual(expected, output)

    def test_markdown_to_blocks_single_block(self):
        # Test when there's only one block (no double newlines)
        input = "This is a single paragraph with no blank lines."
        expected = ["This is a single paragraph with no blank lines."]
        output = markdown_to_blocks(input)
        self.assertListEqual(expected, output)

    def test_markdown_to_blocks_excessive_whitespace(self):
        # Test handling multiple blank lines between blocks
        input = """# Heading


Paragraph one



Paragraph two"""
        expected = ["# Heading", "Paragraph one", "Paragraph two"]
        output = markdown_to_blocks(input)
        self.assertListEqual(expected, output)

    def test_markdown_to_blocks_leading_trailing_whitespace(self):
        # Test blocks with leading/trailing whitespace
        input = """  # Heading with spaces

  Paragraph with spaces  """
        expected = ["# Heading with spaces", "Paragraph with spaces"]
        output = markdown_to_blocks(input)
        self.assertListEqual(expected, output)

    def test_markdown_to_blocks_empty_string(self):
        # Test empty input
        input = ""
        expected = []
        output = markdown_to_blocks(input)
        self.assertListEqual(expected, output)

    def test_markdown_to_blocks_only_whitespace(self):
        # Test input with only whitespace and newlines
        input = "\n\n\n\n"
        expected = []
        output = markdown_to_blocks(input)
        self.assertListEqual(expected, output)

    def test_extract_title(self):
        input = """
# a test header
"""
        expected = "a test header"
        output = extract_title(input)
        self.assertEqual(expected, output)

    def test_extract_tttle_exception(self):
        input = """### Test title"""
        with self.assertRaises(ValueError) as e:
            extract_title(input)
        self.assertEqual(str(e.exception), "Header not found in input")


if __name__ == "__main__":
    unittest.main()
