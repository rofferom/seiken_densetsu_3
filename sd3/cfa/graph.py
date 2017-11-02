import os
import graphviz


class Edge:
    def __init__(self, src, dest):
        self._src = src
        self._dest = dest
        self._attrs = set()

    def add_attr(self, attr):
        self._attrs.add(attr)

    def has_attr(self, attr):
        return attr in self._attrs

    def get_src(self):
        return self._src

    def get_dest(self):
        return self._dest


class Node:
    def __init__(self, id_):
        self._id = id_
        self._successors = []
        self._predecessors = []
        self._data = None

    def get_id(self):
        return self._id

    def set_data(self, data):
        self._data = data

    def get_data(self):
        return self._data

    def add_successor(self, node):
        edge = Edge(self, node)
        self._successors.append(edge)
        node._predecessors.append(edge)

        return edge

    def has_successor(self, node):
        for edge in self._successors:
            if edge.get_dest() is node:
                return True

        return False

    def get_successors(self):
        return self._successors

    def get_predecessors(self):
        return self._predecessors


class Graph:
    def __init__(self):
        self._nodes = {}
        self._entry = None
        self._exit = None

    def _check_node_known(self, node):
        node_id = node.get_id()
        if node_id not in self._nodes:
            raise KeyError("node key isn't in the graph")
        elif self._nodes[node_id] is not node:
            raise KeyError("node isn't in the graph")

    def set_entry(self, node):
        self._check_node_known(node)
        self._entry = node

    def get_entry(self):
        return self._entry

    def set_exit(self, node):
        self._check_node_known(node)
        self._exit = node

    def get_exit(self):
        return self._exit

    def add_node(self, id_):
        if id_ in self._nodes:
            return (self._nodes[id_], False)

        node = Node(id_)
        self._nodes[id_] = node

        return (node, True)

    def has_node(self, id_):
        return id_ in self._nodes

    def get_node(self, id_):
        return self._nodes[id_]

    def get_node_list(self):
        return [self._nodes[k] for k in sorted(self._nodes.keys())]

    def get_node_it(self):
        return self._nodes.items()

    def get_edges_it(self):
        for _, node in self._nodes.items():
            for edge in node.get_successors():
                yield edge

    def draw(self, out_path, *, shape=None, node_id_str=None, node_str=None):
        basename, extension = os.path.splitext(out_path)

        if shape:
            node_attr = {"shape": shape}
        else:
            node_attr = {}

        # Build graph
        dot = graphviz.Digraph(
            format=extension[1:],
            node_attr=node_attr)

        def get_node_id(n):
            return node_id_str(n) if node_id_str else n.get_id()

        # Build nodes
        for _, node in self.get_node_it():
            node_id = get_node_id(node)

            if node_str:
                dot.node(node_id, node_str(node))
            else:
                dot.node(node_id)

        # Build edges
        for edge in self.get_edges_it():
            src_id = get_node_id(edge.get_src())
            dest_id = get_node_id(edge.get_dest())
            dot.edge(src_id, dest_id)

        return dot.render(filename=basename, cleanup=True)
