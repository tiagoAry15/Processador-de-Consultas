import re

from classes.Operation import Operation


class SQLParser:
    def __init__(self, query):
        self.query = query
        self.tokens = []
        self.operations = []
        self.elements = {

            'TABLES': [],
            'PROJECTION': [],
            'WHERE_SELECTION': [],
            'UNION': [],
            'ON_SELECTION': []

        }

    def tokenize(self):
        keywords = r"(Select|from|where|join|on|and|in|not in)"
        operators = r"(\=|>|<|<=|>=|<>\(|\))"
        word = r"(\w+)"
        whitespace = r"(\s+)"
        punctuation = r"([,.])"

        regex = re.compile(
            f"{keywords}|{operators}|{punctuation}|{word}|{whitespace}")
        self.tokens = [token.group() for token in re.finditer(
            regex, self.query) if token.group().strip()]

    def parse(self):
        self.tokenize()

        if self.tokens and self.tokens[0] == "Select":
            self.parse_select()
        else:
            raise ValueError("A consulta SQL deve começar com SELECT")

        return self.elements

    def parse_select(self):
        columns = []

        self.tokens.pop(0)  # Remove 'select'
        while self.tokens and self.tokens[0] != "from":
            columns.append(self.tokens.pop(0))

        if columns:
            self.elements['PROJECTION'] = columns
        else:
            raise ValueError("Nenhuma coluna encontrada após SELECT")

        if self.tokens and self.tokens[0] == "from":
            self.parse_from()
        else:
            raise ValueError("A cláusula FROM não foi encontrada")

    def parse_from(self):
        self.tokens.pop(0)  # Remove 'from'
        if self.tokens and re.match(r'\w+', self.tokens[0]):
            table = self.tokens.pop(0)

            self.elements['TABLES'].append(table)
            if not table:
                raise ValueError("Nenhuma tabela encontrada após FROM")

        if self.tokens:
            if self.tokens[0] == "where":
                self.parse_where()
            elif self.tokens[0] == "join":
                self.elements['UNION'].append(table)
                self.parse_join()

    def parse_where(self):
        self.tokens.pop(0)  # Remove 'where'
        print("Condições WHERE:")
        while self.tokens and self.tokens[0] != "join":
            condition = []
            while self.tokens and self.tokens[0] not in ["and", "join"]:
                condition.append(self.tokens.pop(0))
            condition = ''.join(condition)
            match = re.search(
                r"([\wáéíóúàèìòùâêîôûãõç]+)\s*([=<>]{1,2})\s*([\wáéíóúàèìòùâêîôûãõç]+)", condition)
            if match:
                attr, op, value = match.groups()
                self.elements['WHERE_SELECTION'].append(f"{attr} {op} {value}")

            if self.tokens and self.tokens[0] == "and":
                self.tokens.pop(0)  # Remove 'and'

        if self.tokens and self.tokens[0] == "join":
            self.parse_join()

    def parse_join(self):
        while self.tokens and self.tokens[0] == "join":
            self.tokens.pop(0)  # Remove 'join'
            if self.tokens and re.match(r'\w+', self.tokens[0]):
                table = self.tokens.pop(0)

                self.elements['UNION'].append('|X|')

                self.elements['UNION'].append(table)
                self.elements['TABLES'].append(table)

                if self.tokens and self.tokens[0] == "on":
                    self.parse_on()
                else:
                    raise ValueError(
                        "A cláusula ON não foi encontrada após JOIN")
            else:
                raise ValueError("Nenhuma tabela encontrada após JOIN")

    def parse_on(self):

        self.tokens.pop(0)  # Remove 'on'
        while self.tokens and self.tokens[0] not in ["join"]:
            condition = []
            while self.tokens and self.tokens[0] not in ["and", "join"]:
                if self.tokens and self.tokens[0] == "where":
                    self.parse_where()
                else:
                    condition.append(self.tokens.pop(0))

            condition = [elem if elem != '=' else ' = ' for elem in condition]
            self.elements['ON_SELECTION'].append(''.join(condition))

            if self.tokens and self.tokens[0] == "and":
                self.tokens.pop(0)  # Remove 'and'

        if self.tokens and self.tokens[0] == "join":
            self.parse_join()
