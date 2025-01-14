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

class TestSplitImageLink(TestCase):
	def test_image_node(self):
		node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) bottom text", TextType.NORMAL)
		new_nodes = split_nodes_image([node])
		self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.NORMAL))
		self.assertEqual(new_nodes[1], TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"))
		self.assertEqual(new_nodes[2], TextNode(" and ", TextType.NORMAL))
		self.assertEqual(new_nodes[3], TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"))
		self.assertEqual(new_nodes[4], TextNode(" bottom text", TextType.NORMAL))
	def test_link_node(self):
		node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) bottom text", TextType.NORMAL)
		new_nodes = split_nodes_link([node])
		self.assertEqual(new_nodes[0], TextNode("This is text with a link ", TextType.NORMAL))
		self.assertEqual(new_nodes[1], TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"))
		self.assertEqual(new_nodes[2], TextNode(" and ", TextType.NORMAL))
		self.assertEqual(new_nodes[3], TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"))
		self.assertEqual(new_nodes[4], TextNode(" bottom text", TextType.NORMAL))
	def test_invalid_image_node(self):
		node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) bottom text", TextType.NORMAL)
		new_nodes = split_nodes_image([node])
		self.assertEqual(new_nodes[0], TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif and ", TextType.NORMAL))
		self.assertEqual(new_nodes[1], TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"))
		self.assertEqual(new_nodes[2], TextNode(" bottom text", TextType.NORMAL))
	def test_invalid_link_node(self):
		node = TextNode("This is text with a link [to boot dev](https://www.boot.dev and [to youtube](https://www.youtube.com/@bootdotdev) bottom text", TextType.NORMAL)
		new_nodes = split_nodes_link([node])
		self.assertEqual(new_nodes[0], TextNode("This is text with a link [to boot dev](https://www.boot.dev and ", TextType.NORMAL))
		self.assertEqual(new_nodes[1], TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"))
		self.assertEqual(new_nodes[2], TextNode(" bottom text", TextType.NORMAL))
	def test_image_and_link(self):
		node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to youtube](https://www.youtube.com/@bootdotdev) bottom text", TextType.NORMAL)
		new_nodes = split_nodes_image(split_nodes_link([node]))
		self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.NORMAL))
		self.assertEqual(new_nodes[1], TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"))
		self.assertEqual(new_nodes[2], TextNode(" and ", TextType.NORMAL))
		self.assertEqual(new_nodes[3], TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"))
		self.assertEqual(new_nodes[4], TextNode(" bottom text", TextType.NORMAL))
	def test_image_node_with_delimiter(self):
		node = TextNode("**This is text** with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) bottom text", TextType.NORMAL)
		new_nodes = split_nodes_delimiter(split_nodes_image([node]), "**", TextType.BOLD)
		self.assertEqual(new_nodes[0], TextNode("This is text", TextType.BOLD))
		self.assertEqual(new_nodes[1], TextNode(" with a ", TextType.NORMAL))
		self.assertEqual(new_nodes[2], TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"))
		self.assertEqual(new_nodes[3], TextNode(" and ", TextType.NORMAL))
		self.assertEqual(new_nodes[4], TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"))
		self.assertEqual(new_nodes[5], TextNode(" bottom text", TextType.NORMAL))
	def test_link_node_with_delimiter(self):
		node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) `bottom text`", TextType.NORMAL)
		new_nodes = split_nodes_delimiter(split_nodes_link([node]), "`", TextType.CODE)
		self.assertEqual(new_nodes[0], TextNode("This is text with a link ", TextType.NORMAL))
		self.assertEqual(new_nodes[1], TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"))
		self.assertEqual(new_nodes[2], TextNode(" and ", TextType.NORMAL))
		self.assertEqual(new_nodes[3], TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"))
		self.assertEqual(new_nodes[4], TextNode(" ", TextType.NORMAL))
		self.assertEqual(new_nodes[5], TextNode("bottom text", TextType.CODE))

class TestTextToNodes(TestCase):
	def test_text_to_textnodes(self):
		self.assertEqual(
			text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"),
			[
				TextNode("This is ", TextType.NORMAL),
				TextNode("text", TextType.BOLD),
				TextNode(" with an ", TextType.NORMAL),
				TextNode("italic", TextType.ITALIC),
				TextNode(" word and a ", TextType.NORMAL),
				TextNode("code block", TextType.CODE),
				TextNode(" and an ", TextType.NORMAL),
				TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
				TextNode(" and a ", TextType.NORMAL),
				TextNode("link", TextType.LINK, "https://boot.dev"),
			]
		)
class TestMarkdownToBlocks(TestCase):
	def test_m_to_b(self):
		md = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
		self.assertEqual(
			markdown_to_blocks(md),
			[
				"# This is a heading",
				"This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
				"* This is the first list item in a list block\n* This is a list item\n* This is another list item"
			]
		)

class TestBlocktoBlockType(TestCase):
	def test_headings(self):
		h0 = "not heading"
		h1 = "# heading 1"
		h2 = "## heading 2"
		h3 = "### heading 3"
		h4 = "#### heading 4"
		h5 = "##### heading 5"
		h6 = "###### heading 6"
		h7 = "####### heading 7 (not real)"

		self.assertEqual(block_to_block_type(h0), "normal")
		self.assertEqual(block_to_block_type(h1), "heading")
		self.assertEqual(block_to_block_type(h2), "heading")
		self.assertEqual(block_to_block_type(h3), "heading")
		self.assertEqual(block_to_block_type(h4), "heading")
		self.assertEqual(block_to_block_type(h5), "heading")
		self.assertEqual(block_to_block_type(h6), "heading")
		self.assertEqual(block_to_block_type(h7), "normal")
	def test_code(self):
		code = """```this
		is some
		code```"""
		self.assertEqual(block_to_block_type(code), "code")
	def test_quote(self):
		quote = """> a quote
		>quote continued
		> more quote"""
		self.assertEqual(block_to_block_type(quote), "quote")
	def test_ulist(self):
		ulist = """* a ulist
		- ulist continued
		* more ulist"""
		self.assertEqual(block_to_block_type(ulist), "ulist")
	def test_olist(self):
		olist = """1. a olist
		2. olist continued
		3. more olist"""
		notolist = """1. a olist
		2. olist continued
		3. more olist
		5. out of order whoops"""
		self.assertEqual(block_to_block_type(olist), "olist")
		self.assertEqual(block_to_block_type(notolist), "normal")

class TestExtractMarkdownTitle(TestCase):
	def test_extract_title(self):
		md = """
# Front-end Development is the Worst

Look, front-end development is for `script kiddies` and soydevs who can't handle the real programming. I mean, it's just a bunch of divs and spans, right? And css??? It's like, "Oh, I want this to be red, but not thaaaaat red." What a joke.

Real programmers code, not silly markup languages. They code on Arch Linux, not Mac OS, and certainly not Windows. They use Vim, not VS Code. They use C, not HTML. Come to the [backend](https://www.boot.dev), where the real programming happens.
"""
		self.assertEqual(extract_title(md), "Front-end Development is the Worst")
	
if __name__ == "__main__":
	main()
