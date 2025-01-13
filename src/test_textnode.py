import unittest
from textnode import *
from split_functions import *


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

    def test_split(self):
        node = TextNode("I should be **bold** and you should be *italic*.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("I should be ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" and you should be *italic*.", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_regex_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(result, expected)

    def test_regex_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(result, expected)

    def test_split_images(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(result, expected)
    def test_split_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(result, expected)
    
    def test_split_text(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)" 
        nodes = text_to_textnodes(text)
        for i, n in enumerate(nodes):
            print(f"Node {i}: text='{n.text}', type={n.text_type}, url={n.url}")

if __name__ == "__main__":
    unittest.main()
