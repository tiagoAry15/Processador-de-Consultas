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
posicoes_UNION = []
quant_UNION = 0
for i in range(len(string)):
    if string[i] == "PI(":
        posicoes_PI.append(i)
    if string[i] == "SIGMA(":
        posicoes_SIGMA.append(i)
    for x in range(len(queryTable)):
        if string[i] == detectFolhas.format(query["TABLES"][x]):
            posicoes_TABLES.append(i)
print("Posicoes PI:", posicoes_PI)
print("UNION:", query['UNION'])


for i, elemento in enumerate(query["UNION"]):
    if elemento == "|X|":
        quant_UNION += 1
        posicoes_UNION.append(i)
print(posicoes_UNION)

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

quant = 0
for i in range(len(queryTable)):
    if len(queryTable) > 2:
        if (i + 1) == len(queryTable):
            print('eae')
            save = query['ON_SELECTION'][quant]
            quant += 1
            G.add_edge(posicoes_PI[i + 1], query['ON_SELECTION'][quant])
            G.add_edge(save, query['ON_SELECTION'][quant])
        else:
            G.add_edge(posicoes_PI[i + 1], query['ON_SELECTION'][quant])

    else:
        G.add_edge(posicoes_PI[i + 1], query["ON_SELECTION"][quant])
        G.add_edge(posicoes_PI[i + 1], query["ON_SELECTION"][quant])
        print('eae')
else:
    G.add_edge(query["ON_SELECTION"][quant], posicoes_PI[0])


dfs_tree = nx.dfs_tree(G, source=0)

print(dfs_tree)
nx.draw(G, with_labels=True)
print("Lista de nos: ", list(G.nodes()))
print("Lista de arestas: ", list(G.edges()))
#print(string)
plt.show()

#print(' '.join(optimizer.optimize_query()))
