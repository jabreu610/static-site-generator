import unittest

from textnode import TextNode, TextType
from transform import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
)


class TestTransform(unittest.TestCase):
    def test_text_node_to_html_plain(self):
        node = TextNode("Plain text", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "Plain text")

    def test_text_node_to_html_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_text_node_to_html_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_text_node_to_html_code(self):
        node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>print('Hello')</code>")

    def test_text_node_to_html_link(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://example.com" >Click here</a>',
        )

    def test_text_node_to_html_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        # IMAGE case currently returns empty src and alt values
        self.assertEqual(html_node.to_html(), '<img src="" alt="" ></img>')

    def test_text_node_to_html_link_without_url(self):
        # Edge case: link without URL raises ValueError
        node = TextNode("Click here", TextType.LINK, None)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(
            str(context.exception), "Text nodes of type 'LINK' must include a URL"
        )

    def test_text_node_to_html_empty_text(self):
        # Edge case: empty text content
        node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b></b>")

    def test_text_node_to_html_special_characters(self):
        # Edge case: text with special characters
        node = TextNode('Text with <special> & "characters"', TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), 'Text with <special> & "characters"')

    def test_split_nodes_delimiter(self):
        node = TextNode(
            "This is text with a `code phrase` in the middle", TextType.PLAIN
        )
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code phrase", TextType.CODE),
                TextNode(" in the middle", TextType.PLAIN),
            ],
        )

    def test_split_nodes_delimiter_multiple_delimiters(self):
        # Test with multiple delimited segments in a single node
        node = TextNode("Text with *bold* and *more bold* words", TextType.PLAIN)
        nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertListEqual(
            nodes,
            [
                TextNode("Text with ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("more bold", TextType.BOLD),
                TextNode(" words", TextType.PLAIN),
            ],
        )

    def test_split_nodes_delimiter_non_plain_passthrough(self):
        # Test that non-plain text nodes pass through unchanged
        nodes = [
            TextNode("Already bold", TextType.BOLD),
            TextNode("Plain with `code`", TextType.PLAIN),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertListEqual(
            result,
            [
                TextNode("Already bold", TextType.BOLD),
                TextNode("Plain with ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_split_nodes_delimiter_unmatched(self):
        # Test that unmatched delimiter raises ValueError
        node = TextNode("Text with unmatched `delimiter", TextType.PLAIN)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            str(context.exception), "Input text node should include pairs of delimiter"
        )

    def test_split_nodes_delimiter_adjacent_segments(self):
        # Test with adjacent bold segments (no text between delimiters)
        node = TextNode("Text with *bold1**bold2* words", TextType.PLAIN)
        nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertListEqual(
            nodes,
            [
                TextNode("Text with ", TextType.PLAIN),
                TextNode("bold1", TextType.BOLD),
                TextNode("bold2", TextType.BOLD),
                TextNode(" words", TextType.PLAIN),
            ],
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image_single(self):
        # Test splitting a single image
        node = TextNode(
            "Text before ![alt text](https://example.com/image.png) text after",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.PLAIN),
                TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" text after", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_nodes_image_no_images(self):
        # Test when there are no images in the text
        node = TextNode("Plain text with no images", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("Plain text with no images", TextType.PLAIN)], new_nodes
        )

    def test_split_nodes_image_non_plain_passthrough(self):
        # Test that non-plain nodes pass through unchanged
        nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode(
                "Plain with ![image](https://example.com/pic.png)", TextType.PLAIN
            ),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Bold text", TextType.BOLD),
                TextNode("Plain with ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://example.com/pic.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_single(self):
        # Test splitting a single link
        node = TextNode(
            "Text before [link text](https://example.com) text after",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.PLAIN),
                TextNode("link text", TextType.LINK, "https://example.com"),
                TextNode(" text after", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_nodes_link_multiple(self):
        # Test splitting multiple links
        node = TextNode(
            "Visit [Google](https://google.com) or [GitHub](https://github.com) today",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Visit ", TextType.PLAIN),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" or ", TextType.PLAIN),
                TextNode("GitHub", TextType.LINK, "https://github.com"),
                TextNode(" today", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_nodes_link_no_links(self):
        # Test when there are no links in the text
        node = TextNode("Plain text with no links", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("Plain text with no links", TextType.PLAIN)], new_nodes
        )

    def test_split_nodes_link_non_plain_passthrough(self):
        # Test that non-plain nodes pass through unchanged
        nodes = [
            TextNode("Code text", TextType.CODE),
            TextNode("Plain with [link](https://example.com)", TextType.PLAIN),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Code text", TextType.CODE),
                TextNode("Plain with ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
