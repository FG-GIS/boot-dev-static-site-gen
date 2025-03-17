from textnode import TextNode,TextType
from htmlnode import *
from blocktype import *
import re

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

def block_parser(block: str) -> tuple[list[str],str]:
    type = block_to_block_type(block)
    match type:
        case BlockType.PARAGRAPH:
            return (["p"],re.sub(r"(?m)\n+"," ",block))
        case BlockType.QUOTE:
            out = parse_html_quote(block)
            return (["blockquote"],out)
        case BlockType.UNORDERED_LIST:
            out = parse_html_list(block)
            return (["ul"],out)
        case BlockType.ORDERED_LIST:
            out = parse_html_list(block)
            return (["ol"],out)
        case BlockType.CODE:
            out = parse_html_code(block)
            return (["pre","code"],out)
        case BlockType.HEADING:
            out,h_num = parse_html_heading(block)
            return ([f"h{h_num}"],out)

def parse_html_code(block: str) -> str:
    return re.sub(r"(?m)`{3}\n*","",block)

def parse_html_quote(block: str) -> str:
    return re.sub(r"\n"," ",re.sub(r"(?m)^> ","",block))

def parse_html_list(block: str) -> str:
    lines = block.split("\n")
    new_lines = []
    for l in lines:
        new_lines.append("<li>"+re.sub(r"^\d+\. |^- ","",l)+"</li>")
    return "".join(new_lines)

def parse_html_heading(block: str) -> tuple[str,int]:
    count = 0
    for c in block:
        if c =="#":
            count += 1
        else:
            break
    return (re.sub(r"^\#{1,6}? ","",block),count)

# HELPERS for text_to_textnodes
# |
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
            if new_txt[i] == "":
                continue
            if i % 2 == 0 :
                nodes.append(TextNode(new_txt[i],TextType.TEXT))
                continue
            nodes.append(TextNode(new_txt[i],text_type))
    return nodes
# |
def extract_markdown_images(text) -> list[tuple[str,str]]:
    return re.findall(r"!\[(.+?)\]\((.+?)\)",text)
# |
def extract_markdown_links(text) -> list[tuple[str,str]]:
    return re.findall(r"(?<!!)\[(.+?)\]\((.+?)\)",text)
# |
def split_nodes(old_nodes: 'list[TextNode]',rege,func,type):
    nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            nodes.append(n)
            continue

        images = func(n.text)
        if len(images) == 0:
            nodes.append(n)
            continue
        txt = re.split(rege,n.text)
        for i in range(len(txt)):
            if txt[i] != "":
                nodes.append(TextNode(txt[i],TextType.TEXT))
            if 0 <= i < len(images):
                nodes.append(TextNode(images[i][0],type,images[i][1]))
    return nodes
# |
def split_nodes_image(old_nodes: 'list[TextNode]') -> list[TextNode]:
    return split_nodes(old_nodes, r"!\[.+?\]\(.+?\)", extract_markdown_images,TextType.IMAGE)
# |
def split_nodes_link(old_nodes: 'list[TextNode]') -> list[TextNode]:
    return split_nodes(old_nodes, r"(?<!!)\[.+?\]\(.+?\)", extract_markdown_links,TextType.LINK)
# ^
# |
# HELPERS

def text_to_textnodes(text: str) -> list[TextNode]:
    base_nodes = [TextNode(text,TextType.TEXT)]
    base_nodes = split_nodes_delimiter(base_nodes,"**",TextType.BOLD)
    base_nodes = split_nodes_delimiter(base_nodes,"_",TextType.ITALIC)
    base_nodes = split_nodes_delimiter(base_nodes,"`",TextType.CODE)
    base_nodes = split_nodes_image(base_nodes)
    base_nodes = split_nodes_link(base_nodes)
    return base_nodes

def markdown_to_blocks(md: str) -> list[str]:
    blocks = md.split("\n\n")
    return list(filter(None,map(lambda x: x.strip(),blocks)))


def markdown_to_html_node(md_file: str) -> HTMLNode:
    body = ParentNode("div",[])
    md_blocks = markdown_to_blocks(md_file)
    for tag_l,content in map(block_parser,md_blocks):
        # print(f"content is: {content} ||||| testt")
        # print("tag is: ",tag_l)
        if tag_l[0] == "pre":
            # print(TextNode(content,TextType.CODE))
            # print(ParentNode(tag_l[0],[text_node_to_html_node(TextNode(content,TextType.CODE))]))
            body.children.append(
                ParentNode(tag_l[0],[text_node_to_html_node(TextNode(content,TextType.CODE))]))
            continue
        t_nodes = text_to_textnodes(content)
        h_nodes = list(map(text_node_to_html_node,t_nodes))
        body.children.append(ParentNode(tag_l[0],h_nodes))
    return body