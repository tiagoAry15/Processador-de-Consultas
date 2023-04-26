class Operation:
    def __init__(self, type, code):
        self.type = type
        self.code = code
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"Operation({self.type}, {self.code})"
