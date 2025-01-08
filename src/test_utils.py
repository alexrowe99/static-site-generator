from unittest import TestCase, main

from utils import *
from textnode import TextNode, TextType

class TestTextToHTML(TestCase):
	def test_normal(self):
		node = TextNode("this text is normal", TextType.NORMAL)
		leaf = text_node_to_html_node(node)
		self.assertEqual(leaf.tag, None)
		self.assertEqual(leaf.value, node.text)
	def test_bold(self):
		node = TextNode("this text is bold", TextType.BOLD)
		leaf = text_node_to_html_node(node)
		self.assertEqual(leaf.tag, "b")
		self.assertEqual(leaf.value, node.text)
	def test_italic(self):
		node = TextNode("this text is italic", TextType.ITALIC)
		leaf = text_node_to_html_node(node)
		self.assertEqual(leaf.tag, "i")
		self.assertEqual(leaf.value, node.text)
	def test_code(self):
		node = TextNode("this text is code", TextType.CODE)
		leaf = text_node_to_html_node(node)
		self.assertEqual(leaf.tag, "code")
		self.assertEqual(leaf.value, node.text)
	def test_link(self):
		node = TextNode("this text is link", TextType.LINK, "https://www.google.com")
		leaf = text_node_to_html_node(node)
		self.assertEqual(leaf.tag, "a")
		self.assertEqual(leaf.value, node.text)
		self.assertEqual(leaf.props, {'href': 'https://www.google.com'})
	def test_image(self):
		node = TextNode("this is an image", TextType.IMAGE, "img.png")
		leaf = text_node_to_html_node(node)
		self.assertEqual(leaf.tag, "img")
		self.assertEqual(leaf.value, "")
		self.assertEqual(leaf.props, {'src': 'img.png', 'alt': node.text})
	def test_bad_type(self):
		node = TextNode("this type does not exist", None)
		with self.assertRaises(Exception):
			leaf = text_node_to_html_node(node)

class TestSplitNodes(TestCase):
	def test_bold(self):
		node = TextNode("Test with a node with **some bold text** and some not", TextType.NORMAL)
		split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertEqual(split_nodes[0], TextNode("Test with a node with ", TextType.NORMAL))
		self.assertEqual(split_nodes[1], TextNode("some bold text", TextType.BOLD))
		self.assertEqual(split_nodes[2], TextNode(" and some not", TextType.NORMAL))
	def test_italic(self):
		node = TextNode("Test with a node with *some italic text* and some not", TextType.NORMAL)
		split_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
		self.assertEqual(split_nodes[0], TextNode("Test with a node with ", TextType.NORMAL))
		self.assertEqual(split_nodes[1], TextNode("some italic text", TextType.ITALIC))
		self.assertEqual(split_nodes[2], TextNode(" and some not", TextType.NORMAL))
	def test_code(self):
		node = TextNode("Test with a node with `some code` and some not", TextType.NORMAL)
		split_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertEqual(split_nodes[0], TextNode("Test with a node with ", TextType.NORMAL))
		self.assertEqual(split_nodes[1], TextNode("some code", TextType.CODE))
		self.assertEqual(split_nodes[2], TextNode(" and some not", TextType.NORMAL))
	def test_multiple_same_delim(self):
		node = TextNode("Test with a node with **some bold text** and some not and **a little more bold** and again not", TextType.NORMAL)
		split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertEqual(split_nodes[0], TextNode("Test with a node with ", TextType.NORMAL))
		self.assertEqual(split_nodes[1], TextNode("some bold text", TextType.BOLD))
		self.assertEqual(split_nodes[2], TextNode(" and some not and ", TextType.NORMAL))
		self.assertEqual(split_nodes[3], TextNode("a little more bold", TextType.BOLD))
		self.assertEqual(split_nodes[4], TextNode(" and again not", TextType.NORMAL))
	def test_multiple_diff_delim(self):
		node = TextNode("Test with a node with **some bold text** and some not and *some italic text* and again not", TextType.NORMAL)
		split_nodes = split_nodes_delimiter(split_nodes_delimiter([node], "**", TextType.BOLD), "*", TextType.ITALIC)
		self.assertEqual(split_nodes[0], TextNode("Test with a node with ", TextType.NORMAL))
		self.assertEqual(split_nodes[1], TextNode("some bold text", TextType.BOLD))
		self.assertEqual(split_nodes[2], TextNode(" and some not and ", TextType.NORMAL))
		self.assertEqual(split_nodes[3], TextNode("some italic text", TextType.ITALIC))
		self.assertEqual(split_nodes[4], TextNode(" and again not", TextType.NORMAL))
	def test_invalid(self):
		node = TextNode("This is *text is missing a closing asterisk", TextType.NORMAL)
		with self.assertRaises(Exception):
			split_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

class TestExtractFunctions(TestCase):
	def test_image(self):
		self.assertEqual(extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
	def test_link(self):
		self.assertEqual(extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
	def test_invalid_image(self):
		self.assertEqual(extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"), [("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
	def test_invalid_link(self):
		self.assertEqual(extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev and [to youtube](https://www.youtube.com/@bootdotdev)"), [("to youtube", "https://www.youtube.com/@bootdotdev")])
	def test_image_and_link(self):
		self.assertEqual(extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to youtube](https://www.youtube.com/@bootdotdev)"), [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])
		self.assertEqual(extract_markdown_links("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to youtube](https://www.youtube.com/@bootdotdev)"), [("to youtube", "https://www.youtube.com/@bootdotdev")])
	
if __name__ == "__main__":
	main()
