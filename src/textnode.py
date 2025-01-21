from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode:
    def __init__(self, TEXT, TEXT_TYPE, URL = None):
        self.text = TEXT
        self.text_type = TEXT_TYPE
        self.url = URL

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            node = LeafNode(None, text_node.text)

            return node
        case TextType.BOLD:
            node =  LeafNode('b', text_node.text)

            return node
        case TextType.ITALIC:
            node = LeafNode('i', text_node.text)

            return node
        case TextType.CODE:
            node = LeafNode('code', text_node.text)

            return node
        case TextType.LINK:
            node = LeafNode('a', text_node.text, {"href": text_node.url})

            return node
        case TextType.IMAGE:
            node = LeafNode('img', "", {"src": text_node.url, "alt": text_node.text}) 

            return node
        case _:
            raise Exception


