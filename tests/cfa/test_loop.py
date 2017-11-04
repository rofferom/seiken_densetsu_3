import unittest
import sd3.cfa.graph
import sd3.cfa.dominator
import sd3.cfa.loop

class TestLoop(unittest.TestCase):
    def _build_graph(self):
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

        return (graph, nodes)

    def _create_node_set(self, nodes, id_list):
        node_set = set()

        for i in id_list:
            node_set.add(nodes[i])

        return node_set

    def test(self):
        # Build graph
        (graph, node_set) = self._build_graph()

        # Build its dominator graph
        dom_graph = sd3.cfa.dominator.build_graph(graph)

        # Find loops
        found_loops = sd3.cfa.loop.find_loops(graph, dom_graph)

        # Expected loops
        expected_loop_set = list()

        loop = self._create_node_set(node_set, [3, 4])
        expected_loop_set.append(loop)

        loop = self._create_node_set(node_set, [7, 8, 10])
        expected_loop_set.append(loop)

        loop = self._create_node_set(node_set, [3, 4, 5, 6, 7, 8, 10])
        expected_loop_set.append(loop)

        loop = self._create_node_set(node_set, [3, 4, 5, 6, 7, 8, 10])
        expected_loop_set.append(loop)

        loop = self._create_node_set(node_set,
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        expected_loop_set.append(loop)

        # Check of expected loops has been found
        for loop in found_loops:
            loop.display()
            loop = set(loop.get_node_list())
            expected_loop_set.remove(loop)

        self.assertListEqual(expected_loop_set, [])

    def test_autoloop(self):
        graph = sd3.cfa.graph.Graph()
        nodes = {}

        # Create nodes
        for i in range(1, 5):
            (nodes[i], _) = graph.add_node("%d" % i)

        graph.set_entry(nodes[1])

        # Create edges
        nodes[1].add_successor(nodes[2])

        # Self loop
        nodes[2].add_successor(nodes[3])

        nodes[2].add_successor(nodes[2])

        nodes[3].add_successor(nodes[4])

        # Build its dominator graph
        dom_graph = sd3.cfa.dominator.build_graph(graph)

        # Find loops
        found_loops = sd3.cfa.loop.find_loops(graph, dom_graph)
        self.assertEqual(len(found_loops), 1)

        expected_loop = self._create_node_set(nodes, [2])
        self.assertSetEqual(set(found_loops[0].get_node_list()), expected_loop)
