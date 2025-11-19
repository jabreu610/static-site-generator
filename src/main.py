from textnode import TextNode, TextType


def main():
    node = TextNode("This is anchor text", TextType.LINK, "https://www.example.com")
    print(node)


main()
