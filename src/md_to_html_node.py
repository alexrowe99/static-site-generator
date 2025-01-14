from utils import markdown_to_blocks, block_to_block_type, text_to_textnodes, text_node_to_html_node
from htmlnode import HTMLNode

def text_to_html(text):
	textnodes = text_to_textnodes(text)
	nodes = []
	for textnode in textnodes:
		nodes.append(text_node_to_html_node(textnode))
	return nodes

def heading_to_html(heading):
	headingtype = 0
	while heading[headingtype] == "#":
		headingtype += 1
	content = heading[headingtype+1:]
	children = text_to_html(content)
	return HTMLNode("h"+headingtype, None, children)

def code_to_html(code):
	content = code.split("```")[1]
	children = text_to_html(content)
	return HTMLNode("code", None, children)

def quote_to_html(quote):
	lines = quote.split("> ")
	content = "".join(lines)
	children = text_to_html(content)
	return HTMLNode("blockquote", None, children)

def li_to_html(content):
	children = text_to_html(content)
	return HTMLNode("li", None, children)

def ulist_to_html(ulist):
	lines = ulist.split("\n")
	children = []
	for line in lines:
		children.append(li_to_html(line[2:]))
	return HTMLNode("ul", None, children)

def olist_to_html(ulist):
	lines = ulist.split("\n")
	children = []
	for line in lines:
		children.append(li_to_html(line[line.index('.')+2:]))
	return HTMLNode("ol", None, children)

def md_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	nodes = []
	for block in blocks:
		btype = block_to_block_type(block)
		match (btype):
			case "heading":
				nodes.append(heading_to_html(block))
				break
			case "code":
				nodes.append(code_to_html(block))
				break
			case "quote":
				nodes.append(quote_to_html(block))
				break
			case "ulist":
				nodes.append(ulist_to_html(block))
				break
			case "olist":
				nodes.append(olist_to_html(block))
				break
			case _:
				nodes.append(HTMLNode("p", None, text_to_html(block)))
	return HTMLNode("html", None, [HTMLNode("body", None, nodes)])
	