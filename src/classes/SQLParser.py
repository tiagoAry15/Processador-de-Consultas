import re

from classes.Operation import Operation


class SQLParser:
    def __init__(self, query):
        self.query = query.lower()
        self.tokens = []
        self.operations = []

    def tokenize(self):
        keywords = r"(select|from|where|join|on|and|in|not in)"
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

        if self.tokens and self.tokens[0] == "select":
            self.parse_select()
        else:
            raise ValueError("A consulta SQL deve começar com SELECT")

        return self.operations

    def parse_select(self):
        columns = []

        self.tokens.pop(0)  # Remove 'select'
        while self.tokens and self.tokens[0] != "from":
            columns.append(self.tokens.pop(0))

        if columns:
            print(f"Colunas selecionadas: {' '.join(columns)}")

            projection_op = Operation("PROJECTION", ''.join(columns))
            self.operations.append(projection_op)
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
            self.operations.append(
                Operation('TABLE', ''.join(table)))
        else:
            raise ValueError("Nenhuma tabela encontrada após FROM")

        if self.tokens:
            if self.tokens[0] == "where":
                self.parse_where()
            elif self.tokens[0] == "join":
                self.parse_join()

    def parse_where(self):
        self.tokens.pop(0)  # Remove 'where'
        print("Condições WHERE:")
        while self.tokens and self.tokens[0] != "join":
            condition = []
            while self.tokens and self.tokens[0] not in ["and", "join"]:
                condition.append(self.tokens.pop(0))
            print("  ", " ".join(condition))
            self.operations.append(
                Operation('SELECTION WHERE', ' '.join(condition)))

            if self.tokens and self.tokens[0] == "and":
                self.tokens.pop(0)  # Remove 'and'

        if self.tokens and self.tokens[0] == "join":
            self.parse_join()

    def parse_join(self):
        while self.tokens and self.tokens[0] == "join":
            self.tokens.pop(0)  # Remove 'join'
            if self.tokens and re.match(r'\w+', self.tokens[0]):
                table = self.tokens.pop(0)
                join_op = Operation("UNION", 'X')
                self.operations.append(join_op)
                self.operations.append(
                    Operation('TABLE', ''.join(table)))

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

            on_op = Operation("SELECTION ON", ' '.join(condition))
            self.operations[-1].add_child(on_op)
            self.operations.append(on_op)

            if self.tokens and self.tokens[0] == "and":
                self.tokens.pop(0)  # Remove 'and'

        if self.tokens and self.tokens[0] == "join":
            self.parse_join()


# Exemplo de uso do analisador
