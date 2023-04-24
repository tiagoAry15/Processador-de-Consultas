class Operation:
    def __init__(self, op_type, code):
        self.op_type = op_type
        self.code = code
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"Operation({self.op_type}, {self.code})"
