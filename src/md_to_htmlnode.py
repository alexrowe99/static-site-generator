from utils import markdown_to_blocks, block_to_block_type, text_to_textnodes, text_node_to_html_node
from parentnode import ParentNode

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
	return ParentNode("h"+str(headingtype), children)

def code_to_html(code):
	content = code.split("```")[1]
	children = text_to_html(content)
	return ParentNode("code", children)

def quote_to_html(quote):
	lines = quote.split("> ")
	content = "".join(lines)
	children = text_to_html(content)
	return ParentNode("blockquote", children)

def li_to_html(content):
	children = text_to_html(content)
	return ParentNode("li", children)

def ulist_to_html(ulist):
	lines = ulist.split("\n")
	children = []
	for line in lines:
		children.append(li_to_html(line[2:]))
	return ParentNode("ul", children)

def olist_to_html(ulist):
	lines = ulist.split("\n")
	children = []
	for line in lines:
		children.append(li_to_html(line[line.index('.')+2:]))
	return ParentNode("ol", children)

def md_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	nodes = []
	for block in blocks:
		btype = block_to_block_type(block)
		match (btype):
			case "heading":
				nodes.append(heading_to_html(block))
			case "code":
				nodes.append(code_to_html(block))
			case "quote":
				nodes.append(quote_to_html(block))
			case "ulist":
				nodes.append(ulist_to_html(block))
			case "olist":
				nodes.append(olist_to_html(block))
			case _:
				nodes.append(ParentNode("p", text_to_html(block)))
	return ParentNode("div", nodes)
	