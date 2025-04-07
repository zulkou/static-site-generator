from htmlnode import *
from textnode import *
from split_inline import *

def extract_title(markdown):
    if not markdown.startswith("# "):
        raise Exception
    
    title = markdown.lstrip("# ")
    return title

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
        stripped_line = line.strip()
        if not stripped_line.startswith('>'):
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
        block_type = block_to_block_type(block)
        node = block_to_html_node(block, block_type)
        children.append(node)
    root = ParentNode("div", children, None)
    return root

def block_to_html_node(block, block_type):
    if block_type == "paragraph":
        children = text_to_children(block)
        return ParentNode("p", children, None)
    if block_type == "heading":
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                break
        cleaned = block.lstrip("#").strip(" ")
        children = text_to_children(cleaned)
        return ParentNode(f"h{count}", children, None)
    if block_type == "code":
        code_text = LeafNode(None, block.strip("` "))
        child = [ParentNode("code", [code_text])]
        return ParentNode("pre", child, None)
    if block_type == "ordered_list":
        children = []
        for line in block.split("\n"):
            cleaned = line.lstrip("1234567890.").strip(" ")
            inner_children = text_to_children(cleaned)
            children.append(ParentNode("li", inner_children, None))
        return ParentNode("ol", children, None)
    if block_type == "unordered_list":
        children = []
        for line in block.split("\n"):
            cleaned = line.lstrip("-*").strip(" ")
            inner_children = text_to_children(cleaned)
            children.append(ParentNode("li", inner_children, None))
        return ParentNode("ul", children, None)
    if block_type == "quote":
        lines = block.split("\n")
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('> '):
                cleaned_lines.append(stripped[2:])
            elif stripped.startswith('>'):
                cleaned_lines.append(stripped[1:])
        
        cleaned = "\n".join(cleaned_lines)
        children = text_to_children(cleaned)
        return ParentNode("blockquote", children, None)

def text_to_children(text):
    children = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        try:
            children.append(text_node_to_html_node(textnode))
        except Exception as e:
            print(f"failed to process: {textnode}")
    return children

