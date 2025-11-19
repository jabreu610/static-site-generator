import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(
            "div", [child_node], {"class": "container", "id": "main"}
        )
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main" ><span>child</span></div>',
        )

    def test_to_html_nested_parents(self):
        inner_child = LeafNode("i", "italic")
        middle_parent = ParentNode("span", [inner_child])
        outer_parent = ParentNode("div", [middle_parent], {"class": "wrapper"})
        self.assertEqual(
            outer_parent.to_html(),
            '<div class="wrapper" ><span><i>italic</i></span></div>',
        )

    def test_to_html_mixed_nested_structure(self):
        # Complex nesting: parent with multiple children, some are parents themselves
        node = ParentNode(
            "div",
            [
                LeafNode("h1", "Title"),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold"),
                        LeafNode(None, " and "),
                        LeafNode("i", "Italic"),
                    ],
                ),
                LeafNode("span", "Footer"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><h1>Title</h1><p><b>Bold</b> and <i>Italic</i></p><span>Footer</span></div>",
        )

    def test_to_html_no_tag_raises_error(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode(None, [LeafNode("b", "text")])  # type: ignore
            node.to_html()
        self.assertEqual(str(context.exception), "All parent nodes must have a tag.")

    def test_to_html_no_children_raises_error(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode("div", None)  # type: ignore
            node.to_html()
        self.assertEqual(str(context.exception), "All parent nodes must have children.")

    def test_to_html_empty_children_list(self):
        # Edge case: empty list of children (should work but produce empty tag)
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_single_child(self):
        node = ParentNode("p", [LeafNode("b", "Single")])
        self.assertEqual(node.to_html(), "<p><b>Single</b></p>")

    def test_to_html_deeply_nested(self):
        # Very deep nesting
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [ParentNode("article", [ParentNode("p", [LeafNode("b", "Deep")])])],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><section><article><p><b>Deep</b></p></article></section></div>",
        )


if __name__ == "__main__":
    unittest.main()
