from unittest import TestCase, main

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(TestCase):
	def test_to_html_no_tag(self):
		node = ParentNode(
			None,
			[
				LeafNode("b", "Bold text"),
				LeafNode(None, "Normal text"),
				LeafNode("i", "italic text"),
				LeafNode(None, "Normal text"),
			],
		)
		with self.assertRaises(ValueError):
			html = node.to_html()
	def test_to_html_no_children(self):
		node = ParentNode(
			"p",
			None,
		)
		with self.assertRaises(ValueError):
			html = node.to_html()
	def test_to_html_only_leaf_children(self):
		node = ParentNode(
			"p",
			[
				LeafNode("b", "Bold text"),
				LeafNode(None, "Normal text"),
				LeafNode("i", "italic text"),
				LeafNode(None, "Normal text"),
			],
		)
		self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
	def test_to_html_nested_one_level(self):
		node = ParentNode(
			"p",
			[
				LeafNode("b", "Bold text"),
				LeafNode(None, "Normal text"),
				ParentNode(
					"p",
					[
						LeafNode("b", "Bold text"),
						LeafNode(None, "Normal text"),
						LeafNode("i", "italic text"),
						LeafNode(None, "Normal text"),
					],
				),
				LeafNode(None, "Normal text"),
			],
		)
		self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>Normal text</p>")
	def test_to_html_nested_multiple_levels(self):
		node = ParentNode(
			"p",
			[
				ParentNode(
					"p",
					[
						LeafNode("b", "Bold text"),
						ParentNode(
							"p",
							[
								LeafNode("b", "Bold text"),
								LeafNode(None, "Normal text"),
								LeafNode("i", "italic text"),
								ParentNode(
									"p",
									[
										LeafNode("b", "Bold text"),
										LeafNode(None, "Normal text"),
										LeafNode("i", "italic text"),
										LeafNode(None, "Normal text"),
									],
								),
							],
						),
						ParentNode(
							"p",
							[
								LeafNode("b", "Bold text"),
								LeafNode(None, "Normal text"),
								LeafNode("i", "italic text"),
								LeafNode(None, "Normal text"),
							],
						),
						LeafNode(None, "Normal text"),
					],
				),
				LeafNode(None, "Normal text"),
				LeafNode("i", "italic text"),
				LeafNode(None, "Normal text"),
			],
		)
		self.assertEqual(node.to_html(), "<p><p><b>Bold text</b><p><b>Bold text</b>Normal text<i>italic text</i><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>Normal text</p>Normal text<i>italic text</i>Normal text</p>")

if __name__ == "__main__":
	main()