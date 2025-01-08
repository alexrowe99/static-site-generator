from unittest import TestCase, main

from utils import *
from textnode import TextNode, TextType

class TestUtils(TestCase):
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


if __name__ == "__main__":
	main()
