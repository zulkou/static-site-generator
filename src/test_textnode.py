import unittest
from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq2(self):
        node = TextNode("Is this have URL", TextType.LINK, "https://zulkou.github.io")
        node2 = TextNode("Is this have URL", TextType.LINK, "https://zulkou.github.io")
        self.assertEqual(node, node2)
    def test_eq3(self):
        node = TextNode("This is an Image", TextType.IMAGE)
        node2 = TextNode("This is an Image", TextType.IMAGE)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("Hello, Boots!", TextType.TEXT)
        result = text_node_to_html_node(node).to_html()
        expected = "Hello, Boots!"
        self.assertEqual(result, expected)
    def test_bold(self):
        node = TextNode("Hello, Boots in bold", TextType.BOLD)
        result = text_node_to_html_node(node).to_html()
        expected = "<b>Hello, Boots in bold</b>"
        self.assertEqual(result, expected)
    def test_italic(self):
        node = TextNode("Hello, Boots in italic", TextType.ITALIC)
        result = text_node_to_html_node(node).to_html()
        expected = "<i>Hello, Boots in italic</i>"
        self.assertEqual(result, expected)
    def test_code(self):
        node = TextNode("print('Hello, Boots!')", TextType.CODE)
        result = text_node_to_html_node(node).to_html()
        expected = "<code>print('Hello, Boots!')</code>"
        self.assertEqual(result, expected)
    def test_link(self):
        node = TextNode("Visit Boots Here!", TextType.LINK, "https://www.boot.dev")
        result = text_node_to_html_node(node).to_html()
        expected = "<a href=\"https://www.boot.dev\">Visit Boots Here!</a>"
        self.assertEqual(result, expected)
    def test_image(self):
        node = TextNode("This is boots", TextType.IMAGE, "boots.jpg")
        result = text_node_to_html_node(node).to_html()
        expected = "<img src=\"boots.jpg\" alt=\"This is boots\"></img>"
        self.assertEqual(result, expected)
    def test_text_exc(self):
        node = TextNode("Hey Boots!", None)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()
