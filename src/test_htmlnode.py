import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_html(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        result = node.props_to_html()     
        expected = ' href="https://example.com" target="_blank"'
        self.assertEqual(result, expected)
    def test_html2(self):
        node = HTMLNode(tag="a", value="link", props={"href": "example.com"})
        node2 = HTMLNode(tag="a", value="link", props={"href": "example.com"})
        self.assertEqual(node, node2)
    def test_html3(self):
        nodech = HTMLNode(tag="a", value="link", props={"href": "example.com"})
        node = HTMLNode(tag = "h1", children = [nodech])
        node2 = HTMLNode(tag = "h1", children = [nodech])
        self.assertEqual(node, node2)

    def test_leaf(self):
        node = LeafNode("p", "Nice to meet you, Boots!")
        result = node.to_html()
        expected = "<p>Nice to meet you, Boots!</p>"
        self.assertEqual(expected, result)
    def test_leaf2(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)
    def test_leaf3(self):
        node = LeafNode("a", "boot.dev", {"href": "https://www.boot.dev", "target": "_blank"})
        result = node.to_html()
        expected = "<a href=\"https://www.boot.dev\" target=\"_blank\">boot.dev</a>"
        self.assertEqual(result, expected)
    def test_leaf4(self):
        node = LeafNode(None, "Hi, I'm Boots your trusty companion")
        result = node.to_html()
        expected = "Hi, I'm Boots your trusty companion"
        self.assertEqual(result, expected)

    def test_parent(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        result = node.to_html()
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(result, expected)
    def test_parent2(self):
        node = ParentNode(
            "div", 
            [
                ParentNode(
                    "p", 
                    [
                        LeafNode("b", "Bold text"), 
                        LeafNode(None, "Normal text"),
                    ],
                ), 
                ParentNode(
                    "p", 
                    [
                        LeafNode("i", "Italic text"), 
                        LeafNode("a", "This is a link to idk", {"href": "https://www.anywhere.inc"}),
                    ],
                ),
            ],
        )
        result = node.to_html()
        expected = "<div><p><b>Bold text</b>Normal text</p><p><i>Italic text</i><a href=\"https://www.anywhere.inc\">This is a link to idk</a></p></div>"
        self.assertEqual(result, expected)
    def test_parent3(self):
        node = ParentNode(None, [LeafNode("a", "This is a link to idk", {"href": "https://www.anywhere.inc"})])
        self.assertRaises(ValueError, node.to_html)

if __name__ == "__main__":
    unittest.main()
