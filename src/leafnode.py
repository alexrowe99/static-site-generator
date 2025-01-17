from htmlnode import HTMLNode

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag, value, props=props)
	def to_html(self):
		if not self.value and not self.tag == 'img':
			raise ValueError("No value found")
		if not self.tag:
			return self.value
		if not self.tag == 'img':
			return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
		return f'<img{self.props_to_html()}/>'