from classes.Optimizer import Optimizer
from classes.SQLParser import SQLParser
import networkx as nx
import matplotlib.pyplot as plt


query = "Select idusuario, nome, datanascimento, descricao, saldoinicial, UF, Descrição from usuario join contas on usuario.idUsuario = contas.Usuario_idUsuario join tipoconta on tipoconta.idTipoConta = contas.TipoConta_idTipoConta where saldoinicial < 3000 and uf = 'ce' and Descrição <> 'Conta Corrente' and idusuario > 3;"
parser = SQLParser(query)
# Parse
query = parser.parse()

optimizer = Optimizer(query)

string = optimizer.optimize_query().copy()
queryTable = query["TABLES"]
sub_list = []
detectFolhas = "({})"

G = nx.Graph()
posicoes_PI = []
posicoes_SIGMA = []
posicoes_TABLES = []
for i in range(len(string)):
    if string[i] == "PI(":
        posicoes_PI.append(i)
    if string[i] == "SIGMA(":
        posicoes_SIGMA.append(i)
    for x in range(len(queryTable)):
        if string[i] == detectFolhas.format(query["TABLES"][x]):
            posicoes_TABLES.append(i)
print("Posicoes PI:", posicoes_PI)


for i in range(len(queryTable)):
    bat = string[posicoes_SIGMA[i] : posicoes_TABLES[i]]
    G.add_node(queryTable[i])
    save = queryTable[i]
    for y in range(len(query["WHERE_SELECTION"])):
        for x in range(len(bat)):
            if bat[x] == query["WHERE_SELECTION"][y]:
                G.add_node(bat[x])
                G.add_edge(save, bat[x])
                save = bat[x]

    G.add_edge(save, posicoes_PI[i + 1])
    G.add_edge(posicoes_PI[i + 1], query["ON_SELECTION"][0])
    G.add_edge(posicoes_PI[i + 1], query["ON_SELECTION"][0])
else:
    G.add_edge(query["ON_SELECTION"][0], posicoes_PI[0])

nx.draw(G, with_labels=True)
print("Lista de nos: ", list(G.nodes()))
print("Lista de arestas: ", list(G.edges()))
print(string)
plt.show()

#print(' '.join(optimizer.optimize_query()))
