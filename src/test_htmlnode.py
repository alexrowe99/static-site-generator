from unittest import TestCase, main

from htmlnode import HTMLNode
from unittest.mock import patch
from io import StringIO


class TestHTMLNode(TestCase):
	def test_repr(self):
		node = HTMLNode("img","Test node",props={"href":"img.png"})
		with patch('sys.stdout', new = StringIO()) as fake_out: 
			print(node)
			self.assertEqual(fake_out.getvalue(), "HTMLNode(tag=img, value=Test node, children=None, props={'href': 'img.png'})\n")
	def test_tag(self):
		node = HTMLNode("img","Test node",props={"href":"img.png"})
		self.assertEqual(node.tag, "img")
	def test_value(self):
		node = HTMLNode("img","Test node",props={"href":"img.png"})
		self.assertEqual(node.value, "Test node")
	def test_children(self):
		children = [HTMLNode("img","Test node",props={"href":"img.png"})]
		node = HTMLNode("div","Test node",children)
		self.assertEqual(node.children, children)
	def test_props(self):
		node = HTMLNode("img","Test node",props={"href":"img.png"})
		self.assertEqual(node.props, {'href': 'img.png'})
	def test_props_to_html(self):
		node = HTMLNode("img","Test node",props={"href":"img.png"})
		props = node.props_to_html()
		self.assertEqual(props, " href=\"img.png\"")
	def test_props_to_html_multiple(self):
		node = HTMLNode("img","Test node",props={"href":"img.png", "alt":"an image"})
		props = node.props_to_html()
		self.assertEqual(props, " href=\"img.png\" alt=\"an image\"")
	def test_props_to_html_no_props(self):
		node = HTMLNode("div","Test node")
		props = node.props_to_html()
		self.assertEqual(props, "")

if __name__ == "__main__":
	main()