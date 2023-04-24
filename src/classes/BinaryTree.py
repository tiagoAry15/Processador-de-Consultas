import networkx as nx
import matplotlib.pyplot as plt


class BinaryTree:
    def __init__(self, root=None):
        self.root = root

    def add_nodes_edges(self, op, graph, parent=None):
        graph.add_node(op)
        if parent:
            graph.add_edge(parent, op)
            for child in op.children:
                self.add_nodes_edges(child, graph, op)

    def draw_tree(self):

        G = nx.DiGraph()

        if self.root:
            self.add_nodes_edges(self.root, G, None)

            pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
            nx.draw(G, pos, with_labels=True, node_size=3000,
                    node_color='lightblue', font_size=12)
            plt.show()
        else:
            print("Nenhuma operação encontrada.")
