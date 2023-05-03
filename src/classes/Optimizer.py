from Constantes_tables import find_class_for_attribute, is_attribute_in_class


class Optimizer:
    #Query frase
    #Elements dicionario
    def __init__(self, elements):
        self.elements = elements
        self.query = []
        self.description = []
        pass

    def optimize_query(self):
        self.format_unions()
        self.format_on_selections()
        self.format_where_selections()
        self.format_PI_expressions()
        return self.query

    def format_unions(self):

        for element in self.elements['UNION']:
            if element != '|X|':
                self.query.append('('+element+')')
                self.description.append('TABLE')

                if '|X|' in self.query:
                    self.query.insert(0, '(')
                    self.description.insert(0, '(')

                    self.query.append(')')
                    self.description.append(')')
            else:
                self.query.append(element)
                self.description.append('UNION')

    def format_on_selections(self):
        for condition in self.elements['ON_SELECTION']:
            for j, element in enumerate(self.query):
                if element == '|X|':
                    text_copy = self.query[j +
                                           1].replace("(", "").replace(")", "")
                    if text_copy in condition:
                        self.query.insert(j+1, condition)
                        self.description.insert(j+1, 'ON_CONDITION')
                        break

    def format_where_selections(self):
        for condition in self.elements['WHERE_SELECTION']:
            for i, element in enumerate(self.query):
                if self.description[i] == 'TABLE':
                    table = element.replace("(", "").replace(")", "")
                    atributo = condition.split(' ')[0]
                    if is_attribute_in_class(atributo, table):
                        if self.description[i-1] != "WHERE_CONDITION":

                            self.query.insert(i, "SIGMA(")
                            self.description.insert(i, "SIGMA")

                            self.query.insert(i+1, condition)
                            self.description.insert(i+1, "WHERE_CONDITION")

                            self.query.insert(i+3, ")")
                            self.description.insert(i+3, ")")

                        else:
                            self.query.insert(i, "^")
                            self.description.insert(i, "AND")

                            self.query.insert(i+1, condition)
                            self.description.insert(i+1, "WHERE_CONDITION")
                        break

    def format_PI_expressions(self):
        tables = [[self.query[i].replace("(", "").replace(")", ""), i]
                  for i, element in enumerate(self.description) if element == 'TABLE']

        dict_tables = {table[0]: []
                       for table in tables}
        for table in dict_tables.keys():
            for attribute in self.elements['PROJECTION']:

                if is_attribute_in_class(attribute, table) and attribute not in dict_tables[table]:
                    dict_tables[table].append(attribute)

            for condition in self.elements['WHERE_SELECTION']:
                atribute = condition.split(' ')[0]
                if is_attribute_in_class(atribute, table) and atribute not in dict_tables[table]:
                    dict_tables[table].append(atribute)

            for condition in self.elements['ON_SELECTION']:
                condition_elements = condition.split(' ')
                condition_elements.pop(1)
                for elem in condition_elements:
                    table, atribute = elem.split(".")
                    if atribute not in dict_tables[table]:
                        dict_tables[table].append(atribute)
        checked_tables = {
            table: False for table in self.elements['TABLES']}
        for index, element in enumerate(self.description):
            if not all(checked_tables):
                break
            if element == 'TABLE':
                table = self.query[index].replace("(", "").replace(")", "")
                if not checked_tables[table]:
                    self.query.insert(index+1, ")")
                    self.description.insert(index+1, ")")
                    for j in range(index, -1, -1):
                        if self.query[j-1] == "(" or self.description[j-1] == "ON_CONDITION":
                            for k, value in enumerate(dict_tables[table]):
                                self.query.insert(j, value)
                                self.description.insert(j, "ATTRIBUTE")
                                if k != len(dict_tables[table]) - 1:
                                    self.query.insert(j, ",")
                                    self.description.insert(j, ",")
                            self.query.insert(j, "PI(")
                            self.description.insert(j, "PI(")
                            checked_tables[table] = True
                            break
        self.query.insert(-1, ")")
        for k, value in enumerate(self.elements['PROJECTION']):
            self.query.insert(0, value)
            self.description.insert(0, "ATTRIBUTE")
        self.query.insert(0, "PI(")
        self.description.insert(0, "PI(")
