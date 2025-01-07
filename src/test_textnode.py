from unittest import TestCase, main

from textnode import TextNode, TextType
from unittest.mock import patch
from io import StringIO


class TestTextNode(TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)
	def test_type_not_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.ITALIC)
		self.assertNotEqual(node, node2)
	def test_text_not_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a test node", TextType.BOLD)
		self.assertNotEqual(node, node2)
	def test_repr_no_url(self):
		node = TextNode("Test node", TextType.BOLD)
		with patch('sys.stdout', new = StringIO()) as fake_out: 
			print(node)
			self.assertEqual(fake_out.getvalue(), "TextNode(Test node, bold, None)\n")
	def test_repr_url(self):
		node = TextNode("Test node", TextType.BOLD, "https://www.google.com")
		with patch('sys.stdout', new = StringIO()) as fake_out: 
			print(node)
			self.assertEqual(fake_out.getvalue(), "TextNode(Test node, bold, https://www.google.com)\n") 
	def test_text(self):
		node = TextNode("Test node", TextType.BOLD)
		self.assertEqual(node.text, "Test node")
	def test_type(self):
		node = TextNode("Test node", TextType.BOLD)
		self.assertEqual(node.text_type, TextType.BOLD)
	def test_url_none(self):
		node = TextNode("Test node", TextType.BOLD)
		self.assertEqual(node.url, None)
	def test_url(self):
		node = TextNode("Test node", TextType.BOLD, "https://www.google.com")
		self.assertEqual(node.url, "https://www.google.com")

if __name__ == "__main__":
	main()