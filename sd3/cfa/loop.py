from sd3.cfa.dominator import dominates


class Loop:
    def __init__(self):
        self._nodes = []

    def add_node(self, node):
        self._nodes.append(node)

    def get_node_list(self):
        return self._nodes

    def has_node(self, node):
        return node in self._nodes

    def display(self):
        sorted_nodes = list(self._nodes)
        sorted_nodes.sort(key=lambda n: n.get_id())

        for i, node in enumerate(sorted_nodes):
            if i == 0:
                s = node.get_id()
            else:
                s += ", %s" % node.get_id()

        print(s)


class _Finder:
    def __init__(self, graph, dom_graph):
        self.graph = graph
        self.dom_graph = dom_graph

    def _find_back_edges(self):
        back_edges = []

        for edge in self.graph.get_edges_it():
            dom_src = self.dom_graph.get_node(edge.get_src().get_id())
            dom_dest = self.dom_graph.get_node(edge.get_dest().get_id())

            if dominates(dom_dest, dom_src):
                back_edges.append(edge)

        return back_edges

    def _find_natural_loop(self, edge):
        loop = Loop()
        loop.add_node(edge.get_src())
        loop.add_node(edge.get_dest())

        stack = []
        stack.append(edge.get_src())

        while stack:
            node = stack.pop()

            for pred_edge in node.get_predecessors():
                pred = pred_edge.get_src()

                if not loop.has_node(pred):
                    loop.add_node(pred)
                    stack.append(pred)

        return loop

    def _find_auto_loops(self):
        loops = []

        for _, node in self.graph.get_node_it():
            if node.has_successor(node):
                loop = Loop()
                loop.add_node(node)

                loops.append(loop)

        return loops

    def run(self):
        # Find auto-loops
        loops = self._find_auto_loops()

        # Find natural loops
        back_edges = self._find_back_edges()
        for edge in back_edges:
            loop = self._find_natural_loop(edge)
            loops.append(loop)

        return loops


def find_loops(graph, dom_graph):
    finder = _Finder(graph, dom_graph)
    return finder.run()
