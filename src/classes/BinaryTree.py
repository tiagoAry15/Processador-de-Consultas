import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


class BinaryTree:
    def __init__(self, operations):
        self.operations = operations
        self.graph = nx.DiGraph()
        self.graph = nx.Graph(self.graph)
        self.root = operations[0]
        self.build_graph()

    def build_graph(self):
        enumerated_op = enumerate(self.operations)
        previous_op = None
        for index, op in enumerated_op:
            if op.type == "SELECTION WHERE":
                self.add_selection_where_node(index)

            if op.type == "SELECTION ON":
                self.add_selection_on_node(index)

            if op.type == "UNION":
                self.add_union_node(index)

            if op.type == "PROJECTION":
                self.graph.add_node(op)
                if previous_op:
                    self.graph.add_edge(op, previous_op)
            previous_op = op

    def add_selection_where_node(self, index):
        new_node = self.operations[index]
        nodes = list(self.graph.nodes)
        node = nodes[0]
        if node is None:
            raise ValueError("Nó raiz não encontrado")

        node_neighbors = list(self.graph.neighbors(node))

        # Adicionar o novo nó ao grafo e atualizar as conexões
        self.graph.add_node(new_node)

        for neighbor in node_neighbors:
            self.graph.remove_edge(node, neighbor)
            self.graph.add_edge(new_node, neighbor)

        self.graph.add_edge(node, new_node)

    def add_selection_on_node(self, index):
        new_node = self.operations[index]
        nodes = list(self.graph.nodes)
        start_node = nodes[-1]
        if start_node is None:
            raise ValueError("Nó raiz não encontrado")

        self.bfs_add_node(start_node, new_node)

    def add_union_node(self, index):

        self.graph.add_node(self.operations[index])
        self.graph.add_node(self.operations[index-1])
        self.graph.add_node(self.operations[index+1])

        self.graph.add_edge(list(self.graph.nodes)[0], self.operations[index])
        self.graph.add_edge(self.operations[index-1], self.operations[index])
        self.graph.add_edge(self.operations[index+1], self.operations[index])

    def bfs_add_node(self, start_node, new_node):
        visited = set()
        queue = deque([start_node])

        while queue:
            current_node = queue.popleft()

            if current_node not in visited:
                visited.add(current_node)

                if current_node.code in new_node.code and current_node.type == 'TABLE':
                    self.graph.add_node(new_node)
                    node_neighbors = list(self.graph.neighbors(
                        current_node))
                    for neighbor in node_neighbors:
                        self.graph.remove_edge(
                            current_node, neighbor)
                        self.graph.add_edge(new_node, neighbor)
                        self.graph.add_edge(
                            new_node, current_node)

                for neighbor in self.graph.neighbors(current_node):
                    if neighbor not in visited:
                        queue.append(neighbor)

    def display(self):
        def get_tree_positions(G, root):
            levels = {root: 0}
            queue = deque([root])

            while queue:
                current_node = queue.popleft()

                for neighbor in G.neighbors(current_node):
                    if neighbor not in levels:
                        levels[neighbor] = levels[current_node] + 1
                        queue.append(neighbor)

            # Incluir todos os nós que não estão conectados ao nó raiz com nível 0
            for node in G.nodes:
                if node not in levels:
                    levels[node] = 0

            pos = {}
            max_level = max(levels.values())
            for node, level in levels.items():
                x = (level + 1) / (max_level + 2)
                y = (level + 1) * (2 / (G.out_degree(node) + 2))
                pos[node] = (x, y)

            return pos

        #
        pos = nx.spring_layout(self.graph, seed=42)

        # Ajuste o atributo do rótulo aqui
        labels = {node: node.code for node in self.graph.nodes}

        nx.draw(self.graph, pos, with_labels=True, labels=labels,
                node_color="lightblue", font_size=10, font_weight="bold", node_size=2000)

        plt.show()
