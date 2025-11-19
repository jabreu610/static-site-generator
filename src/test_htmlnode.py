import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        out = HTMLNode(
            "a", "test", None, {"href": "https://www.google.com", "target": "__blank"}
        )
        expected = ' href="https://www.google.com" target="__blank" '
        self.assertEqual(out.props_to_html(), expected)

    def test_props_to_html_empty(self):
        out = HTMLNode("div", "content")
        expected = ""
        self.assertEqual(out.props_to_html(), expected)

    def test_repr(self):
        node = HTMLNode("p", "paragraph text", None, {"class": "text-bold"})
        expected = "HTMLNode(p, paragraph text, None, {'class': 'text-bold'})"
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
