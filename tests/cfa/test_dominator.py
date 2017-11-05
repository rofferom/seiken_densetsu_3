import os
import tempfile
import unittest
import sd3.cfa.graph
import sd3.cfa.dominator

class TestDominator(unittest.TestCase):
    def test(self):
        graph = sd3.cfa.graph.Graph()
        nodes = {}

        # Create nodes
        for i in range(1, 12):
            (nodes[i], _) = graph.add_node("%d" % i)

        graph.set_entry(nodes[1])

        # Create edges
        nodes[1].add_successor(nodes[2])
        nodes[1].add_successor(nodes[3])

        nodes[2].add_successor(nodes[3])

        nodes[3].add_successor(nodes[4])

        nodes[4].add_successor(nodes[3])
        nodes[4].add_successor(nodes[5])
        nodes[4].add_successor(nodes[6])

        nodes[5].add_successor(nodes[7])

        nodes[6].add_successor(nodes[7])

        nodes[7].add_successor(nodes[3])
        nodes[7].add_successor(nodes[8])

        nodes[8].add_successor(nodes[9])
        nodes[8].add_successor(nodes[10])

        nodes[9].add_successor(nodes[11])

        nodes[10].add_successor(nodes[3])
        nodes[10].add_successor(nodes[7])
        nodes[10].add_successor(nodes[11])

        nodes[11].add_successor(nodes[1])

        # Build dominator tree
        dom_graph = sd3.cfa.dominator.build_graph(graph)

        nodes = {}

        # Create nodes
        for i in range(1, 12):
            nodes[i] = dom_graph.get_node("%d" % i)

        node_list = list(nodes)
        self._test_successors(node_list, nodes[1], [nodes[2], nodes[3]])
        self._test_successors(node_list, nodes[2], [])
        self._test_successors(node_list, nodes[3], [nodes[4]])
        self._test_successors(node_list, nodes[4], [nodes[5], nodes[6], nodes[7]])
        self._test_successors(node_list, nodes[5], [])
        self._test_successors(node_list, nodes[6], [])
        self._test_successors(node_list, nodes[7], [nodes[8]])
        self._test_successors(node_list, nodes[8], [nodes[9], nodes[10], nodes[11]])
        self._test_successors(node_list, nodes[9], [])
        self._test_successors(node_list, nodes[10], [])
        self._test_successors(node_list, nodes[11], [])

        # Test dominates function
        self.assertTrue(sd3.cfa.dominator.dominates(nodes[1], nodes[2]))
        self.assertTrue(sd3.cfa.dominator.dominates(nodes[1], nodes[5]))
        self.assertTrue(sd3.cfa.dominator.dominates(nodes[1], nodes[11]))

        self.assertTrue(sd3.cfa.dominator.dominates(nodes[4], nodes[9]))

        self.assertFalse(sd3.cfa.dominator.dominates(nodes[5], nodes[7]))

        self.assertFalse(sd3.cfa.dominator.dominates(nodes[10], nodes[8]))

        self.assertFalse(sd3.cfa.dominator.dominates(nodes[2], nodes[1]))

        # Run draw to test that the function doesn't crash
        (fd, path) = tempfile.mkstemp(suffix=".png")
        sd3.cfa.dominator.draw_graph(dom_graph, path)

    def _test_successors(self, node_list, node, successors):
        for successor in successors:
            self.assertTrue(node.has_successor(successor))

        for not_successor in node_list:
            if not_successor in successors:
                continue

            self.assertFalse(node.has_successor(not_successor))
