from htmlnode import HTMLNode

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, children=children, props=props)
	def to_html(self):
		if not self.tag:
			raise ValueError("No tag found")
		if not self.children:
			raise ValueError("No children found")
		html = f"<{self.tag}{self.props_to_html()}>"
		for child in self.children:
			html += child.to_html()
		html += f"</{self.tag}>"
		return html
