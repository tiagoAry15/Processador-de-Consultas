class Optimizer:

    def __init__(self, elements):
        self.elements = elements
        self.query = []
        pass

    def optimize_query(self):
        self.format_unions()
        self.format_on_selections()
        return self.query

    def format_unions(self):

        for element in self.elements['UNION']:
            if element != '|X|':
                self.query.append('('+element+')')
                if '|X|' in self.query:
                    self.query.insert(0, '(')
                    self.query.append(')')
            else:
                self.query.append(element)

    def format_on_selections(self):
        for condition in self.elements['ON_SELECTION']:
            for j, element in enumerate(self.query):
                if element == '|X|':
                    text_copy = self.query[j +
                                           1].replace("(", "").replace(")", "")
                    if text_copy in condition:
                        self.query.insert(j+1, condition)
                        break

    def format_where_selections(self):
        pass
