from unittest import TestCase, main

from md_to_htmlnode import md_to_html_node

class TestMarkdownToHTML(TestCase):
	def test_md_to_html(self):
		text = """
# Front-end Development is the Worst

Look, front-end development is for `script kiddies` and soydevs who can't handle the real programming. I mean, it's just a bunch of divs and spans, right? And css??? It's like, "Oh, I want this to be red, but not thaaaaat red." What a joke.

Real programmers code, not silly markup languages. They code on Arch Linux, not Mac OS, and certainly not Windows. They use Vim, not VS Code. They use C, not HTML. Come to the [backend](https://www.boot.dev), where the real programming happens.
"""
		file = open("test.html", "w")
		expected = open("expected.html", "r")
		file.write(md_to_html_node(text).to_html())
		file.close()
		file = open("test.html", "r")
		self.assertEqual(file.read(), expected.read())
		file.close()
		expected.close()