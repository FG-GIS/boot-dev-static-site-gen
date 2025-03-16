
class HTMLNode():
    def __init__(self, tag: str = None,
                 value: str = None,
                 children: 'list[HTMLNode]' = None,
                 props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return " "+" ".join(map(lambda k: f"{k}=\"{self.props[k]}\"",self.props))

    def __repr__(self):
        return f"tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self,tag: str, value: str, props: dict = None):
        super().__init__(tag,value,None,props)
    
    def to_html(self):
        if self.value == "":
            raise ValueError("no value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"