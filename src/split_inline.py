from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            result.append(node)
            continue

        splitted = node.text.split(delimiter)

        if len(splitted) % 2 == 0:
            raise Exception("Invalid markdown syntax")

        result.extend(
            TextNode(split, TextType.TEXT if i % 2 == 0 else text_type)
            for i, split in enumerate(splitted)
            if split
        )
    return result

def extract_markdown_images(text):
    result = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def extract_markdown_links(text):
    result = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            result.append(node)
            continue
        
        text_track = node.text
        for alt_text, url in images:
            split_node = text_track.split(f"![{alt_text}]({url})", 1)
            if split_node[0]:
                result.append(TextNode(split_node[0], TextType.TEXT))
            result.append(TextNode(alt_text, TextType.IMAGE, url))
            text_track = split_node[1]
        
        if text_track:
            result.append(TextNode(text_track, TextType.TEXT))
    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            result.append(node)
            continue
       
        text_track = node.text
        for link_text, url in links:
            split_node = text_track.split(f"[{link_text}]({url})", 1)
            if split_node[0]:
                result.append(TextNode(split_node[0], TextType.TEXT))
            result.append(TextNode(link_text, TextType.LINK, url))
            text_track = split_node[1]

        if text_track:
            result.append(TextNode(text_track, TextType.TEXT))
    return result

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    delimiters = [("**", TextType.BOLD), ("*", TextType.ITALIC), ("_", TextType.ITALIC), ("`", TextType.CODE)]
    for delimiter, text_type in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    return nodes
