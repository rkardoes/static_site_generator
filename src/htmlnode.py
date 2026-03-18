class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
       self.tag = tag
       self.value = value
       self.children = children
       self.props = props

    def to_html(self):
        raise NotImplementedError("function not implemented in child class of class HTMLNode")

    def props_to_html(self):
        if not self.props:
            return ''
        formatted_props = ' '.join(f'{key}="{val}"' for key, val in self.props.items())
        return formatted_props
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(self, tag, value, props)

    def to_html(self):
        if not self.value:
            raise ValueError("all leaf nodes must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}>{self.value}</{self.tag}>"
