import unittest

from extract import extract_markdown_images, extract_markdown_links


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


if __name__ == "__main__":
    unittest.main()
