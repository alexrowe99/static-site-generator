class HTMLNode():
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props
	def to_html(self):
		raise NotImplementedError("to_html not implemented for parent class HTMLNode; Use child classes ParentNode or LeafNode")
	def props_to_html(self):
		attr = ""
		if self.props:
			for prop in self.props:
				attr += f' {prop}="{self.props[prop]}"'
		return attr
	def __repr__(self):
		return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'