from textnode import TextNode,TextType
from htmlnode import *

def text_node_to_html_node(text_node: 'TextNode'):
    data = text_node.text
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,data)
        case TextType.BOLD:
            return LeafNode("b",data)
        case TextType.ITALIC:
            return LeafNode("i",data)
        case TextType.CODE:
            return LeafNode("code",data)
        case TextType.LINK:
            return LeafNode("a",data,{"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img","",{"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("unknown TextType")

def split_nodes_delimiter(old_nodes: 'list[TextNode]', delimiter: str, text_type: 'TextType') -> list[TextNode]:
    nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            nodes.append(n)
            continue
        
        new_txt = n.text.split(delimiter)
        if len(new_txt) % 2 == 0:
            raise Exception(f"delimiter ->{delimiter} not matched\n node text: {n.text}")
        for i in range(len(new_txt)):
            if i % 2 == 0:
                nodes.append(TextNode(new_txt[i],TextType.TEXT))
                continue
            nodes.append(TextNode(new_txt[i],text_type))
    return nodes