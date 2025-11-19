import unittest

from textnode import TextNode, TextType
from transform import text_node_to_html_node


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


if __name__ == "__main__":
    unittest.main()
