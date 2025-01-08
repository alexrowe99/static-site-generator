from textnode import TextNode, TextType
from leafnode import LeafNode

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
			if idx % 2 == 0:
				new_nodes.append(TextNode(new_values[idx], node.text_type))
			else:
				new_nodes.append(TextNode(new_values[idx], text_type))
	return new_nodes