from unittest import TestCase, main

from leafnode import LeafNode

class TestLeafNode(TestCase):
	def test_to_html_no_value(self):
		node = LeafNode("p", None)
		with self.assertRaises(ValueError):
			html = node.to_html()
	def test_to_html_no_tag(self):
		node = LeafNode(None, "This is raw text")
		self.assertEqual(node.to_html(), node.value)
	def test_to_html_no_props(self):
		node = LeafNode("p", "This is a paragraph with no props")
		self.assertEqual(node.to_html(), "<p>This is a paragraph with no props</p>")
	def test_to_html_props(self):
		node = LeafNode("a", "This is an anchor with an href attribute", {'href': 'https://www.google.com'})
		self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">This is an anchor with an href attribute</a>")

if __name__ == "__main__":
	main()