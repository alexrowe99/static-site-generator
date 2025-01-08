from textnode import TextNode, TextType
from leafnode import LeafNode
import re

def text_node_to_html_node(text_node):
	match text_node.text_type:
		case TextType.NORMAL:
			return LeafNode(None, text_node.text)
		case TextType.BOLD:
			return LeafNode("b", text_node.text)
		case TextType.ITALIC:
			return LeafNode("i", text_node.text)
		case TextType.CODE:
			return LeafNode("code", text_node.text)
		case TextType.LINK:
			return LeafNode("a", text_node.text, {'href':text_node.url})
		case TextType.IMAGE:
			return LeafNode("img", "", {'src':text_node.url, 'alt':text_node.text})
		case _:
			raise Exception("Text type not found")
def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for node in old_nodes:
		new_values = node.text.split(delimiter)
		if len(new_values) % 2 == 0:
			raise Exception(f"Invalid markdown syntax, no matching {delimiter}")
		for idx in range(len(new_values)):
			if idx % 2 == 0 and len(new_values[idx]) > 0:
				new_nodes.append(TextNode(new_values[idx], node.text_type, node.url))
			elif idx % 2 != 0:
				new_nodes.append(TextNode(new_values[idx], text_type))
	return new_nodes
def extract_markdown_images(text):
	images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return images
def extract_markdown_links(text):
	links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return links
def split_nodes_image(old_nodes):
	new_nodes = []
	for node in old_nodes:
		images = extract_markdown_images(node.text)
		start_index = 0
		for image in images:
			inline_image = f'![{image[0]}]({image[1]})'
			inline_image_index = node.text.index(inline_image)
			if inline_image_index > start_index:
				new_nodes.append(TextNode(node.text[start_index:inline_image_index], node.text_type, node.url))
			new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
			start_index = inline_image_index+len(inline_image)
		new_nodes.append(TextNode(node.text[start_index:], node.text_type, node.url))
	return new_nodes
def split_nodes_link(old_nodes):
	new_nodes = []
	for node in old_nodes:
		links = extract_markdown_links(node.text)
		start_index = 0
		for link in links:
			inline_link = f'[{link[0]}]({link[1]})'
			new_nodes.append(TextNode(node.text[start_index:node.text.index(inline_link)], node.text_type, node.url))
			new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
			start_index = node.text.index(inline_link)+len(inline_link)
		if start_index < len(node.text):
			new_nodes.append(TextNode(node.text[start_index:], node.text_type, node.url))
	return new_nodes
def text_to_textnodes(text):
	node = TextNode(text, TextType.NORMAL)
	return split_nodes_link(
		split_nodes_image(
			split_nodes_delimiter(
				split_nodes_delimiter(
					split_nodes_delimiter(
						[node],
						"**",
						TextType.BOLD
					),
					"*",
					TextType.ITALIC
				),
				"`",
				TextType.CODE
			)
		)
	)
def markdown_to_blocks(markdown):
	blocks = markdown.split("\n\n")
	for block in blocks:
		if block == "":
			blocks.remove(block)
			continue
		blocks[blocks.index(block)] = block.strip()
	return blocks
	