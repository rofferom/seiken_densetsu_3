import sys
import os
import tempfile
import unittest
import sd3.cfa.graph
import sd3.cfa.shortestpath

class TestGraph(unittest.TestCase):
    def test_edge(self):
        node_src_id = 1
        node_dest_id = 2

        node_src = sd3.cfa.graph.Node(node_src_id)
        node_dest = sd3.cfa.graph.Node(node_dest_id)

        # Test creation
        edge = sd3.cfa.graph.Edge(node_src, node_dest)
        self.assertIs(edge.get_src(), node_src)
        self.assertIs(edge.get_dest(), node_dest)

        # Test attributes
        first_attr = "a"
        second_attr = "b"

        self.assertFalse(edge.has_attr(first_attr))
        self.assertFalse(edge.has_attr(second_attr))

        edge.add_attr(first_attr)
        self.assertTrue(edge.has_attr(first_attr))
        self.assertFalse(edge.has_attr(second_attr))

        edge.add_attr(second_attr)
        self.assertTrue(edge.has_attr(first_attr))
        self.assertTrue(edge.has_attr(second_attr))

    def test_node(self):
        node_src_id = 1
        node_dest_id = 2
        node_data = "Fake data"

        node_src = sd3.cfa.graph.Node(node_src_id)

        # Test initial state
        self.assertEqual(node_src.get_id(), node_src_id)

        self.assertIsNone(node_src.get_data())

        self.assertListEqual(node_src.get_successors(), [])
        self.assertListEqual(node_src.get_predecessors(), [])

        # Test data
        node_src.set_data(node_data)
        self.assertEqual(node_src.get_data(), node_data)

        # Test successor add
        node_dest = sd3.cfa.graph.Node(node_dest_id)
        self.assertFalse(node_src.has_successor(node_dest))

        node_src.add_successor(node_dest)
        self.assertTrue(node_src.has_successor(node_dest))
        self.assertFalse(node_dest.has_successor(node_src))

        successors = node_src.get_successors()
        self.assertEqual(len(successors), 1)
        self.assertIs(successors[0].get_src(), node_src)
        self.assertIs(successors[0].get_dest(), node_dest)

        predecessors = node_dest.get_predecessors()
        self.assertEqual(len(predecessors), 1)
        self.assertIs(predecessors[0].get_src(), node_src)
        self.assertIs(predecessors[0].get_dest(), node_dest)

    def test_node_loop(self):
        node = sd3.cfa.graph.Node(1)

        node.add_successor(node)

        successors = node.get_successors()
        predecessors = node.get_predecessors()

        self.assertEqual(len(successors), 1)
        self.assertEqual(len(predecessors), 1)

        self.assertIs(successors[0].get_src(), node)
        self.assertIs(successors[0].get_dest(), node)

        self.assertIs(predecessors[0].get_src(), node)
        self.assertIs(predecessors[0].get_dest(), node)

    def test_graph(self):
        node_id = 1
        second_node_id = 2
        third_node_id = 2

        # New graph is empty
        graph = sd3.cfa.graph.Graph()
        self.assertIsNone(graph.get_entry())
        self.assertEqual(len(graph.get_node_list()), 0)

        # Forbid entry set on an unknown node
        node = sd3.cfa.graph.Node(node_id)
        self.assertRaises(KeyError, graph.set_entry, node)
        self.assertRaises(KeyError, graph.set_exit, node)

        # Test node add
        (node, is_new) = graph.add_node(node_id)
        self.assertEqual(node.get_id(), node_id)
        self.assertTrue(is_new)
        self.assertTrue(graph.has_node(node_id))

        # Test node add with the same id
        (existing_node, is_new) = graph.add_node(node_id)
        self.assertEqual(existing_node.get_id(), node_id)
        self.assertFalse(is_new)

        # Test that node can be fetched
        self.assertIs(graph.get_node(node_id), node)

        # Test set entry with an invalid node
        fake_node = sd3.cfa.graph.Node(node_id)
        self.assertRaises(KeyError, graph.set_entry, fake_node)
        self.assertRaises(KeyError, graph.set_exit, fake_node)

        # Test valid entry set
        graph.set_entry(node)
        self.assertIs(graph.get_entry(), node)

        # Test valid exit set
        graph.set_exit(node)
        self.assertIs(graph.get_exit(), node)

        # Test node list
        (second_node, _) = graph.add_node(second_node_id)
        self.assertListEqual(graph.get_node_list(), [node, second_node])

        # Test node iterator
        nodes_id = set()
        nodes_it = set()
        for it_node_id, it_node in graph.get_node_it():
            nodes_id.add(it_node_id)
            nodes_it.add(it_node)

        self.assertSetEqual(nodes_id, {node_id, second_node_id})
        self.assertSetEqual(nodes_it, {node, second_node})

        # Test edges
        (third_node, _) = graph.add_node(third_node_id)

        node.add_successor(second_node)
        second_node.add_successor(third_node)

        edge_set = set()
        for edge in list(graph.get_edges_it()):
            edge_set.add((edge.get_src(), edge.get_dest()))

        expected_edge_set = set()
        expected_edge_set.add((node, second_node))
        expected_edge_set.add((second_node, third_node))

        self.assertSetEqual(edge_set, expected_edge_set)

        # Run draw to test that the function doesn't crash
        node_id_str = lambda n: "%s" % n.get_id()
        (fd, path) = tempfile.mkstemp(suffix=".png")
        graph.draw(path, node_id_str=node_id_str)

        os.close(fd)
        os.remove(path)

    def test_shortest_path(self):
        graph = sd3.cfa.graph.Graph()

        # Create nodes
        (node1, _) = graph.add_node(1)
        (node2, _) = graph.add_node(2)
        (node3, _) = graph.add_node(3)
        (node4, _) = graph.add_node(4)
        (node5, _) = graph.add_node(5)
        (node6, _) = graph.add_node(6)
        (node7, _) = graph.add_node(7)

        # Create edges
        node1.add_successor(node2)
        node1.add_successor(node5)
        node1.add_successor(node7)

        node2.add_successor(node3)
        node2.add_successor(node4)

        node3.add_successor(node4)
        node3.add_successor(node7)

        node5.add_successor(node3)
        node5.add_successor(node5)
        node5.add_successor(node6)

        node7.add_successor(node6)

        # Check some paths
        self.assertEqual(sd3.cfa.shortestpath.get(graph, node1, node3), 2)
        self.assertEqual(sd3.cfa.shortestpath.get(graph, node1, node4), 2)
        self.assertEqual(sd3.cfa.shortestpath.get(graph, node1, node6), 2)
        self.assertEqual(sd3.cfa.shortestpath.get(graph, node1, node7), 1)

        self.assertEqual(sd3.cfa.shortestpath.get(graph, node2, node4), 1)
        self.assertEqual(
            sd3.cfa.shortestpath.get(graph, node2, node1),
            sd3.cfa.shortestpath.INFINITE)

        self.assertEqual(sd3.cfa.shortestpath.get(graph, node5, node6), 1)
