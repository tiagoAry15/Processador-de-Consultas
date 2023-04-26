
from classes.BinaryTree import BinaryTree
from classes.SQLParser import SQLParser


query = "Select nome, datanascimento, descricao, saldoinicial from usuario join contas on usuario.idUsuario = contas.Usuario_idUsuario where saldoinicial >=235 and uf ='ce' and cep <> '62930000';"
parser = SQLParser(query)
# Parse
operations = parser.parse()
print(operations)
tree = BinaryTree(operations)
tree.display()
