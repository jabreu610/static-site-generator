import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Link", {"href": "https://www.example.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com" >Link</a>')

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", {"src": "image.png", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.png" alt="An image" ></img>')

    def test_leaf_node_without_tag(self):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_node_with_tag(self):
        node = LeafNode("p", "paragraph content")
        self.assertEqual(node.to_html(), "<p>paragraph content</p>")

    def test_leaf_node_with_tag_and_props(self):
        node = LeafNode(
            "a", "Click here", {"href": "https://example.com", "target": "_blank"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com" target="_blank" >Click here</a>',
        )


if __name__ == "__main__":
    unittest.main()
