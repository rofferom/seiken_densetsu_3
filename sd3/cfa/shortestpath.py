import sys

INFINITE = sys.maxsize


class _ShortestPathAlgo:
    class Node:
        def __init__(self, graph_node, dist):
            self.graph_node = graph_node
            self.dist = dist

    def __init__(self, graph, src, dst):
        self.graph = []
        self.node_map = {}

        self.src = src
        self.dst = dst
        self._build_nodes(graph)

    def _build_nodes(self, graph):
        for node in graph.get_node_list():
            if node is self.src:
                int_node = _ShortestPathAlgo.Node(node, 0)
                self.src = int_node
            elif node is self.dst:
                int_node = _ShortestPathAlgo.Node(node, INFINITE)
                self.dst = int_node
            else:
                int_node = _ShortestPathAlgo.Node(node, INFINITE)

            self.graph.append(int_node)
            self.node_map[node] = int_node

    def _nodes_without_src(self):
        for node in self.graph:
            if node is self.src:
                continue

            yield node

    def _update_successors_dist(self, node):
        for graph_successor in node.graph_node.get_successors():
            successor = self.node_map[graph_successor.get_dest()]

            # Skip self-loop
            if successor is node:
                continue

            successor.dist = min(successor.dist, node.dist+1)

    def run(self):
        # Create required data
        unvisited_nodes = set()
        for node in self._nodes_without_src():
            unvisited_nodes.add(node)

        cur_node = self.src

        while True:
            # Update all successors dist
            self._update_successors_dist(cur_node)

            if cur_node is self.dst:
                break
            elif cur_node in unvisited_nodes:
                unvisited_nodes.remove(cur_node)

            cur_node = min(unvisited_nodes, key=lambda n: n.dist)

        return self.dst.dist


def get(graph, src, dst):
    algo = _ShortestPathAlgo(graph, src, dst)
    return algo.run()
