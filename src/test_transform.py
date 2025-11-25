import unittest

from textnode import TextNode, TextType
from transform import (
    markdown_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
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
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://example.com/image.png" alt="Alt text" ></img>',
        )

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

    def test_text_to_textnodes_plain(self):
        # Test plain text with no markdown
        nodes = text_to_textnodes("Just plain text")
        self.assertListEqual([TextNode("Just plain text", TextType.PLAIN)], nodes)

    def test_text_to_textnodes_bold(self):
        # Test text with bold formatting
        nodes = text_to_textnodes("This is **bold** text")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.PLAIN),
            ],
            nodes,
        )

    def test_text_to_textnodes_italic(self):
        # Test text with italic formatting
        nodes = text_to_textnodes("This is _italic_ text")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.PLAIN),
            ],
            nodes,
        )

    def test_text_to_textnodes_code(self):
        # Test text with code formatting
        nodes = text_to_textnodes("This is `code` text")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.PLAIN),
            ],
            nodes,
        )

    def test_text_to_textnodes_image(self):
        # Test text with image
        nodes = text_to_textnodes("This is ![an image](https://example.com/image.png)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("an image", TextType.IMAGE, "https://example.com/image.png"),
            ],
            nodes,
        )

    def test_text_to_textnodes_link(self):
        # Test text with link
        nodes = text_to_textnodes("This is [a link](https://example.com)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("a link", TextType.LINK, "https://example.com"),
            ],
            nodes,
        )

    def test_text_to_textnodes_mixed_formatting(self):
        # Test text with multiple different formatting types
        nodes = text_to_textnodes("This is **bold** and _italic_ and `code` text")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.PLAIN),
            ],
            nodes,
        )

    def test_text_to_textnodes_complex(self):
        # Test complex text with all formatting types
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_multiple_same_type(self):
        # Test with multiple instances of the same formatting type
        nodes = text_to_textnodes("**bold1** and **bold2** and **bold3**")
        self.assertListEqual(
            [
                TextNode("bold1", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("bold2", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("bold3", TextType.BOLD),
            ],
            nodes,
        )

    def test_text_to_textnodes_sequential_processing(self):
        # Test that formatting is processed sequentially (bold first, then code)
        # The `code` backticks inside **bold** are processed after bold is split
        nodes = text_to_textnodes("Text with **bold and `code`** together")
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.PLAIN),
                TextNode("bold and `code`", TextType.BOLD),
                TextNode(" together", TextType.PLAIN),
            ],
            nodes,
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_to_html_node_heading(self):
        # Test heading conversion
        md = "## This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>This is a heading</h2></div>")

    def test_markdown_to_html_node_multiple_headings(self):
        # Test multiple headings with different levels
        md = """# Main Title

## Subtitle

### Section"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main Title</h1><h2>Subtitle</h2><h3>Section</h3></div>",
        )

    def test_markdown_to_html_node_quote(self):
        # Test blockquote conversion
        md = "> This is a quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote</blockquote></div>")

    def test_markdown_to_html_node_unordered_list(self):
        # Test unordered list conversion
        md = """- Item 1
- Item 2
- Item 3"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"
        )

    def test_markdown_to_html_node_ordered_list(self):
        # Test ordered list conversion
        md = """1. First
2. Second
3. Third"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )

    def test_markdown_to_html_node_mixed_blocks(self):
        # Test document with multiple different block types
        md = """# Title

This is a paragraph with **bold** text.

> A wise quote

- List item 1
- List item 2"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>This is a paragraph with <b>bold</b> text.</p><blockquote>A wise quote</blockquote><ul><li>List item 1</li><li>List item 2</li></ul></div>",
        )

    def test_markdown_to_html_node_empty_string(self):
        # Test with empty markdown
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_markdown_to_html_node_only_whitespace(self):
        # Test with only whitespace
        md = "\n\n\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")


if __name__ == "__main__":
    unittest.main()
