__author__ = 'Acko'

import unittest
from graph.vertex_and_edge import Vertex
from graph.graph import Graph


class MyTestCase(unittest.TestCase):

    def setUp(self):
        # It is all same with non-directed graph, test of vertex and edge covered that
        self.graph = Graph(True)
        self.test_vertex = Vertex("A", directed=True)
        self.graph._nodes["A"] = self.test_vertex
        self.test_vertex2 = Vertex("C", directed=True)
        self.graph._nodes["C"] = self.test_vertex2

    def tearDown(self):
        self.graph = None

    def test_get_node_all_cases(self):
        # may or may not be true, because of order (dictionary doesn't keep order)
        # self.assertEqual(self.graph.get_all_nodes(), [self.test_vertex, self.test_vertex2])
        self.assertIs(self.graph.get_node("A"), self.test_vertex)
        self.assertIsNone(self.graph.get_node("B"))
        self.assertIs(self.graph["A"], self.test_vertex)

        with self.assertRaises(Exception):
            self.graph["B"]

    def test_add_node(self):
        v = Vertex("B", directed=True)

        self.graph._add_node(v)
        # self.assertEqual(self.graph.get_all_nodes(), [self.test_vertex, self.test_vertex2, v])
        self.assertIs(self.graph.get_node("B"), v)
        self.assertIs(self.graph["B"], v)

        with self.assertRaises(TypeError):
            self.graph._add_node("D")

    def test_node_connecting(self):

        self.graph.connect_nodes(self.test_vertex, self.test_vertex2)

        self.assertEqual(self.test_vertex.get_number_of_edges(where_to=Vertex.OUTGOING), 1)
        self.assertEqual(self.test_vertex.get_all_connected_nodes(where_to=Vertex.OUTGOING), [self.graph["C"]])
        self.assertEqual(self.test_vertex.get_number_of_edges(where_to=Vertex.INCOMING), 0)
        self.assertEqual(self.graph.get_node("C").get_number_of_edges(where_to=Vertex.OUTGOING), 0)
        self.assertEqual(self.graph.get_node("C").get_number_of_edges(where_to=Vertex.INCOMING), 1)
        self.assertEqual(self.graph.get_node("C").get_all_connected_nodes(where_to=Vertex.INCOMING), [self.test_vertex])

        self.graph.connect_nodes(self.graph["C"], self.graph["A"])

        self.assertEqual(self.test_vertex.get_number_of_edges(where_to=Vertex.OUTGOING), 1)
        self.assertEqual(self.test_vertex.get_all_connected_nodes(where_to=Vertex.OUTGOING), [self.graph["C"]])
        self.assertEqual(self.test_vertex.get_number_of_edges(where_to=Vertex.INCOMING), 1)
        self.assertEqual(self.graph.get_node("C").get_number_of_edges(where_to=Vertex.OUTGOING), 1)
        self.assertEqual(self.graph.get_node("C").get_number_of_edges(where_to=Vertex.INCOMING), 1)
        self.assertEqual(self.graph.get_node("C").get_all_connected_nodes(where_to=Vertex.INCOMING), [self.test_vertex])

    def test_node_connecting_fails_and_both_ways(self):

        self.graph.connect_both_ways(self.test_vertex, self.test_vertex2)

        self.assertEqual(self.test_vertex.get_number_of_edges(where_to=Vertex.OUTGOING), 1)
        self.assertEqual(self.test_vertex.get_all_connected_nodes(where_to=Vertex.OUTGOING), [self.graph["C"]])
        self.assertEqual(self.test_vertex.get_number_of_edges(where_to=Vertex.INCOMING), 1)
        self.assertEqual(self.graph.get_node("C").get_number_of_edges(where_to=Vertex.OUTGOING), 1)
        self.assertEqual(self.graph.get_node("C").get_number_of_edges(where_to=Vertex.INCOMING), 1)
        self.assertEqual(self.graph.get_node("C").get_all_connected_nodes(where_to=Vertex.INCOMING), [self.test_vertex])

        with self.assertRaises(Exception):
            self.graph.connect_nodes(self.test_vertex, self.test_vertex2)

        with self.assertRaises(TypeError):
            self.graph.connect_nodes("A", "C")

        with self.assertRaises(Exception):
            self.graph.connect_both_ways(self.test_vertex, Vertex("B"))

    def test_exists_and_direction(self):
        self.assertTrue(self.graph.is_directed())
        self.assertTrue(self.graph.exists("A"))
        self.assertFalse(self.graph.exists("B"))

    def test_create_node(self):
        self.graph.create_node("B")

        self.assertTrue(self.graph.exists("B"))

        with self.assertRaises(Exception):
            self.graph.create_node("B")

    def test_remove_node(self):
        self.graph.create_node("B")
        self.graph.create_node("D")

        self.graph.connect_nodes(self.graph["A"], self.graph["B"])
        self.graph.connect_nodes(self.graph["A"], self.graph["D"])
        self.graph.connect_nodes(self.graph["B"], self.graph["C"])
        self.graph.connect_nodes(self.graph["D"], self.graph["B"])

        self.assertEqual(self.graph["A"].get_number_of_edges(where_to=Vertex.OUTGOING), 2)
        self.assertEqual(self.graph["A"].get_number_of_edges(where_to=Vertex.INCOMING), 0)
        self.assertEqual(self.graph["B"].get_number_of_edges(where_to=Vertex.OUTGOING), 1)
        self.assertEqual(self.graph["B"].get_number_of_edges(where_to=Vertex.INCOMING), 2)
        self.assertEqual(self.graph["C"].get_number_of_edges(where_to=Vertex.OUTGOING), 0)
        self.assertEqual(self.graph["C"].get_number_of_edges(where_to=Vertex.INCOMING), 1)
        self.assertEqual(self.graph["D"].get_number_of_edges(where_to=Vertex.OUTGOING), 1)
        self.assertEqual(self.graph["D"].get_number_of_edges(where_to=Vertex.INCOMING), 1)

        self.graph.remove_node("D")

        self.assertEqual(self.graph["A"].get_number_of_edges(where_to=Vertex.OUTGOING), 1)
        self.assertEqual(self.graph["A"].get_number_of_edges(where_to=Vertex.INCOMING), 0)
        self.assertEqual(self.graph["B"].get_number_of_edges(where_to=Vertex.OUTGOING), 1)
        self.assertEqual(self.graph["B"].get_number_of_edges(where_to=Vertex.INCOMING), 1)
        self.assertEqual(self.graph["C"].get_number_of_edges(where_to=Vertex.OUTGOING), 0)
        self.assertEqual(self.graph["C"].get_number_of_edges(where_to=Vertex.INCOMING), 1)

        with self.assertRaises(KeyError):
            self.graph["D"]

        with self.assertRaises(KeyError):
            self.graph.remove_node("D")

if __name__ == '__main__':
    unittest.main()
