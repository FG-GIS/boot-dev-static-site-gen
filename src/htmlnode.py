
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
        if self.value == None:
            raise ValueError("no value")
        if not self.tag:
            return self.value
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()} />"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: 'list[HTMLNode]', props: dict = None):
        super().__init__(tag= tag, children= children,props= props)

    def to_html(self):
        if self.tag == "" or not self.tag:
            raise ValueError("tag cannot be empty or none")
        if not self.children:
            raise ValueError("parentNode must have a child")
        return f"<{self.tag}{self.props_to_html()}>{''.join(map(lambda x: x.to_html(),self.children))}</{self.tag}>"