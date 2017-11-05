import logging
import collections
from collections import namedtuple
import sd3.cfa.graph
import sd3.cfa.shortestpath

_NodeDist = namedtuple("NodeDist", ["node", "dist"])


class _DomNode:
    def __init__(self, graph_node):
        self._graph_node = graph_node
        self._dominators = None

    def get_id(self):
        return self._graph_node.get_id()

    def get_graph_node(self):
        return self._graph_node

    def get_dominators(self):
        return self._dominators

    def set_dominators(self, dominators):
        self._dominators = dominators

    def remove_dominator(self, dominator):
        self._dominators.remove(dominator)


class _GraphBuilder:
    def __init__(self, graph):
        self.graph = graph
        self.nodes = []
        self.node_map = {}
        self.entry_node = None

    def _add_node(self, graph_node):
        node = _DomNode(graph_node)
        self.nodes.append(node)
        self.node_map[graph_node] = node
        return node

    def _get_node_from_graph_node(self, graph_node):
        return self.node_map[graph_node]

    def _create_nodes(self):
        # Create entry node
        graph_entry = self.graph.get_entry()
        self.entry_node = self._add_node(graph_entry)

        # Create the other nodes
        for graph_node in self.graph.get_node_list():
            if graph_node is graph_entry:
                continue

            self._add_node(graph_node)

        # Build the dominator lists
        self.entry_node.set_dominators([self.entry_node])

        for node in self._nodes_without_entry():
            node.set_dominators(list(self.nodes))

    def _nodes_without_entry(self):
        for node in self.nodes:
            if node is self.entry_node:
                continue

            yield node

    def _node_predecessors(self, node):
        graph_node = node.get_graph_node()

        for i, graph_pred in enumerate(graph_node.get_predecessors()):
            pred = self._get_node_from_graph_node(graph_pred.get_src())
            logging.debug("Node %s has predecessor %s",
                          node.get_id(), pred.get_id())
            yield (i, pred)

    def _build_predecessor_dominators(self, node):
        for i, pred in self._node_predecessors(node):
            pred_doms = pred.get_dominators()
            logging.debug("Predecessor %i as %d dominators", i, len(pred_doms))
            if i == 0:
                intersect = set(pred_doms)
            else:
                intersect = intersect & set(pred_doms)

        return intersect

    def _build_dominators(self):
        changes_found = True
        while changes_found:
            changes_found = False

            for node in self._nodes_without_entry():
                # Build intersection of predecessor dominators
                pred_doms = self._build_predecessor_dominators(node)
                # Add current node to the intersection
                pred_doms.add(node)

                # Check if there is a change if the dominator list of the node
                node_dom_set = set(node.get_dominators())

                # Update dominator list if required
                if pred_doms ^ node_dom_set:
                    node.set_dominators(list(pred_doms))
                    changes_found = True

    def _build_dominators_graph(self):
        graph = sd3.cfa.graph.Graph()

        node_map = {}

        # Create nodes
        for node in self.nodes:
            (graph_node, _) = graph.add_node(node.get_id())

            parent_node = node.get_graph_node()
            graph_node.set_data(parent_node.get_data())
            node_map[node] = graph_node

        # Create edges
        for node in self.nodes:
            graph_node = node_map[node]

            for dom in node.get_dominators():
                graph_dom = node_map[dom]
                graph_dom.add_successor(graph_node)

        graph.set_entry(node_map[self.entry_node])

        return graph

    def _filter_closest_dominators(self):
        for node in self._nodes_without_entry():
            graph_node = self.graph.get_node(node.get_id())

            dist_list = []
            for dom in node.get_dominators():
                dom_node = self.graph.get_node(dom.get_id())

                dist = sd3.cfa.shortestpath.get(
                    self.graph, dom_node, graph_node)

                dist_list.append(_NodeDist(dom, dist))

            node_dist = min(dist_list, key=lambda t: t[1])
            node.set_dominators([node_dist.node])

    def _build_dominator_tree(self):
        # Remove self-link
        for node in self.nodes:
            node.remove_dominator(node)

        # Keep only the closest dominators
        self._filter_closest_dominators()

    def run(self):
        self._create_nodes()
        self._build_dominators()
        self._build_dominator_tree()

        return self._build_dominators_graph()


def build_graph(graph):
    builder = _GraphBuilder(graph)
    return builder.run()


def _append_successors(node, queue):
    for edge in node.get_successors():
        queue.append(edge.get_dest())


def dominates(src, dest):
    queue = collections.deque()

    # Init queue
    _append_successors(src, queue)

    while queue:
        node = queue.popleft()
        if node is dest:
            return True

        _append_successors(node, queue)

    return False


def draw_graph(graph, out_path, *, node_str=None):
    return graph.draw(out_path, shape="box", node_str=node_str)
