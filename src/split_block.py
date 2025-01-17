from htmlnode import *
from textnode import *
from split_inline import *

def markdown_to_blocks(markdown):
    doc = markdown.split("\n")
    result = []
    curr = ""
    for line in doc:
        stripped = line.strip()
        if not stripped:
            if curr:
                result.append(curr)
            curr = ""
        else:
            if curr:
                curr += "\n"
            curr += stripped
    if curr:
        result.append(curr)

    return result

def block_to_block_type(block):
    if block.startswith("#"):
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                if char == " ":
                    return "heading"
                break 

    if block.startswith("```") and block.endswith("```"):
        return "code"
    
    lines = block.split("\n")

    ordered_list = True
    for i, line in enumerate(lines):
        expect_start = f"{i + 1}. "
        if not line.startswith(expect_start):
            ordered_list = False
            break
    if ordered_list:
        return "ordered_list"

    all_quotes = True
    for line in lines:
        if not line.startswith('> '):
            all_quotes = False
            break
    if all_quotes:
        return "quote"
        
    all_unordered = True
    for line in lines:
        if not (line.startswith('* ') or line.startswith('- ')):
            all_unordered = False
            break
    if all_unordered:
        return "unordered_list"

    return "paragraph"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        node = block_to_html_node(block, block_to_block_type(block))
        children.append(node)
    return HTMLNode("div", None, children)

def block_to_html_node(block, block_type):
    if block_type == "paragraph":
        children = text_to_children(block)
        return HTMLNode("p", None, children)
    if block_type == "heading":
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                break
        cleaned = block.lstrip("#").strip(" ")
        children = text_to_children(cleaned)
        return HTMLNode(f"h{count}", None, children)
    if block_type == "code":
        child = [HTMLNode("code", block.strip("` "))]
        return HTMLNode("pre", None, child)
    if block_type == "ordered_list":
        children = []
        for line in block.split("\n"):
            cleaned = line.lstrip("1234567890.").strip(" ")
            inner_children = text_to_children(cleaned)
            children.append(HTMLNode("li", None, inner_children))
        return HTMLNode("ol", None, children)
    if block_type == "unordered_list":
        children = []
        for line in block.split("\n"):
            cleaned = line.lstrip("-* ").strip(" ")
            inner_children = text_to_children(cleaned)
            children.append(HTMLNode("li", None, inner_children))
        return HTMLNode("ul", None, children)
    if block_type == "quote":
        cleaned = block.lstrip(">").strip(" ")
        children = text_to_children(cleaned)
        return HTMLNode("blockquote", None, children)

def text_to_children(text):
    children = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        try:
            children.append(text_node_to_html_node(textnode))
        except Exception as e:
            print(f"failed to process: {textnode}")
    return children

