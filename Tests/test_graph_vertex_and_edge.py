__author__ = 'Acko'

import unittest

from graph.vertex_and_edge import Vertex, Edge


class MyTestCase(unittest.TestCase):

    def test_vertex_creation(self):
        v = Vertex('V1')

        self.assertTrue(isinstance(v, Vertex))
        self.assertEqual(v.get_key(), 'V1')
        self.assertEqual(v.get_data(), None)
        self.assertFalse(v.is_directed())
        self.assertIs(v._outgoing, v._incoming)
        self.assertEqual(v.get_number_of_edges(), 0)

        v2 = Vertex('V2', directed=True)

        self.assertTrue(isinstance(v2, Vertex))
        self.assertEqual(v2.get_key(), 'V2')
        self.assertEqual(v2.get_data(), None)
        self.assertTrue(v2.is_directed())
        self.assertIsNot(v2._outgoing, v2._incoming)
        self.assertEqual(v2.get_number_of_edges(), 0)

    def test_vertex_data(self):
        v = Vertex("V1", data="Some random data")

        self.assertTrue(v.has_data())
        self.assertEqual(v.get_data(), "Some random data")

        v2 = Vertex("V2")

        self.assertFalse(v2.has_data())
        self.assertEqual(v2.get_data(), None)

        v2.set_data(123)

        self.assertTrue(v2.has_data())
        self.assertEqual(v2.get_data(), 123)

        v.set_data(v2)

        self.assertEqual(v.get_data(), v2)
        self.assertEqual(v.get_data().get_data(), v2.get_data())

    def test_edge_creation(self):
        v1 = Vertex("A")
        v2 = Vertex("B")
        e = Edge(v1, v2)

        self.assertEqual(e.get_start_vertex(), v1)
        self.assertEqual(e.get_end_vertex(), v2)
        self.assertFalse(e.has_data())
        self.assertEqual(e.return_other_side(v1), v2)
        self.assertEqual(e.return_other_side(v2), v1)

        with self.assertRaises(TypeError):
            Edge("A", "B")

        with self.assertRaises(TypeError):
            Edge(1, 2)

    def test_edge_data_manipulation(self):
        v1 = Vertex("A")
        v2 = Vertex("B")
        e = Edge(v1, v2)
        e2 = Edge(v2, v1, data="Some random data")

        self.assertFalse(e.has_data())
        self.assertTrue(e2.has_data())
        self.assertEqual(e2.get_data(), "Some random data")

        e.set_data(123)
        self.assertTrue(e.has_data())
        self.assertEqual(e.get_data(), 123)

    def test_vertex_add_link(self):
        v1 = Vertex("A", directed=True)
        v2 = Vertex("B", directed=False)
        edge = Edge(v1, v2)

        v1.add_link(edge, where_to=Vertex.OUTGOING)
        v2.add_link(edge, where_to=Vertex.INCOMING)
        self.assertEqual(v1.get_number_of_edges(where_to=Vertex.OUTGOING), 1)
        self.assertEqual(v1.get_all_connected_nodes(where_to=Vertex.OUTGOING), [v2])
        self.assertEqual(v2.get_number_of_edges(), 1)
        self.assertEqual(v2.get_all_connected_nodes(), [v1])

        with self.assertRaises(TypeError):
            v1.add_link(Vertex("C"))
        with self.assertRaises(TypeError):
            v1.add_link("ASDF")

        with self.assertRaises(Exception):
            v1.add_link(edge, where_to=Vertex.INCOMING)
        with self.assertRaises(Exception):
            v2.add_link(edge, where_to=Vertex.OUTGOING)

        # Already connected
        with self.assertRaises(Exception):
            v1.add_link(edge, where_to=Vertex.OUTGOING)
        with self.assertRaises(Exception):
            v2.add_link(edge, where_to=Vertex.INCOMING)

    def test_vertex_connection_undirected(self):
        v1 = Vertex("A")
        v2 = Vertex("B")

        self.assertEqual(v1.get_number_of_edges(), 0)
        self.assertEqual(v2.get_number_of_edges(), 0)

        v1.connect_to_node(v2)

        self.assertEqual(v1.get_number_of_edges(), 1)
        self.assertEqual(v2.get_number_of_edges(), 1)

        self.assertEqual(len(v1.get_all_connected_nodes()), 1)
        self.assertEqual(len(v2.get_all_connected_nodes()), 1)
        self.assertIs(v1.get_all_connected_nodes()[0], v2)
        self.assertIs(v2.get_all_connected_nodes()[0], v1)

        v3 = Vertex("C")
        v4 = Vertex("D")
        v1.connect_to_node(v3)
        v1.connect_to_node(v4)

        self.assertEqual(v1.get_number_of_edges(), 3)
        self.assertEqual(len(v1.get_all_connected_nodes()), 3)
        self.assertEqual(v1.get_all_connected_nodes(), [v2, v3, v4])

    def test_vertex_connection_directed(self):
        v1 = Vertex("A", directed=True)
        v2 = Vertex("B", directed=True)

        v1.connect_to_node(v2, where_to=Vertex.OUTGOING)

        self.assertEqual(v1.get_number_of_edges(where_to=Vertex.INCOMING), 0)
        self.assertEqual(v1.get_number_of_edges(where_to=Vertex.OUTGOING), 1)
        self.assertEqual(v2.get_number_of_edges(where_to=Vertex.INCOMING), 1)
        self.assertEqual(v2.get_number_of_edges(where_to=Vertex.OUTGOING), 0)

        self.assertEqual(v1.get_all_connected_nodes(where_to=Vertex.INCOMING), [])
        self.assertEqual(v1.get_all_connected_nodes(where_to=Vertex.OUTGOING), [v2])
        self.assertEqual(v2.get_all_connected_nodes(where_to=Vertex.INCOMING), [v1])
        self.assertEqual(v2.get_all_connected_nodes(where_to=Vertex.OUTGOING), [])

        v3 = Vertex("C", directed=True)
        v4 = Vertex("D", directed=False)

        v1.connect_to_node(v3, Vertex.INCOMING)
        v1.connect_to_node(v4, Vertex.OUTGOING)

        self.assertEqual(v1.get_all_connected_nodes(where_to=Vertex.INCOMING), [v3])
        self.assertEqual(v1.get_all_connected_nodes(where_to=Vertex.OUTGOING), [v2, v4])
        self.assertEqual(v3.get_all_connected_nodes(where_to=Vertex.INCOMING), [])
        self.assertEqual(v3.get_all_connected_nodes(where_to=Vertex.OUTGOING), [v1])

        # Showing that if vertex is not directed it returns same list for any parameter
        self.assertEqual(v4.get_all_connected_nodes(), [v1])
        self.assertEqual(v4.get_all_connected_nodes(where_to=Vertex.OUTGOING), [v1])
        self.assertEqual(v4.get_all_connected_nodes(where_to=Vertex.INCOMING), [v1])

    def test_vertex_connection_errors(self):
        v1 = Vertex("A")
        v2 = Vertex("B", directed=True)

        with self.assertRaises(TypeError):
            v1.connect_to_node("B")

        with self.assertRaises(TypeError):
            v2.connect_to_node("A")

        with self.assertRaises(TypeError):
            v1.connect_to_node(1)

        with self.assertRaises(TypeError):
            v2.connect_to_node(True)

        with self.assertRaises(TypeError):
            v1.connect_to_node(Edge(v1, v2))

    def test_getting_edges_from_vertex(self):
        v1 = Vertex("A", directed=True)
        v2 = Vertex("B")
        v3 = Vertex("C", directed=True)

        v1.connect_to_node(v2)
        v1.connect_to_node(v3)
        v2.connect_to_node(v3, where_to=Vertex.INCOMING)

        self.assertEqual(len(v1.get_all_edges(where_to=Vertex.OUTGOING)), 2)
        self.assertEqual(len(v1.get_all_edges(where_to=Vertex.INCOMING)), 0)
        self.assertEqual(len(v2.get_all_edges()), v2.get_number_of_edges())
        self.assertEqual(len(v3.get_all_edges(where_to=Vertex.OUTGOING)),
                         v3.get_number_of_edges(where_to=Vertex.OUTGOING))
        self.assertEqual(len(v3.get_all_edges(where_to=Vertex.INCOMING)),
                         v3.get_number_of_edges(where_to=Vertex.INCOMING))

        v4 = Vertex("D", directed=True)
        e1 = Edge(v4, v1)
        e2 = Edge(v4, v3)
        e3 = Edge(v2, v4)

        v4.add_link(e1)
        v4.add_link(e2)
        v4.add_link(e3, where_to=Vertex.INCOMING)

        self.assertEqual(v4.get_all_edges(), [e1, e2])
        self.assertEqual(v4.get_all_edges(where_to=Vertex.INCOMING), [e3])

        self.assertIs(v4.get_edge(v1), e1)
        self.assertIsNone(v4.get_edge(v2))
        self.assertIs(v4.get_edge(v2, where_to=Vertex.INCOMING), e3)

    def test_disconnect_node(self):
        v1 = Vertex("A", directed=True)
        v2 = Vertex("B", directed=True)
        v3 = Vertex("C", directed=True)

        # v2 <- v1 <=> v3
        v1.connect_to_node(v2)
        v1.connect_to_node(v3, where_to=Vertex.OUTGOING)
        v1.connect_to_node(v3, where_to=Vertex.INCOMING)

        self.assertEqual(v1.get_number_of_edges(where_to=Vertex.OUTGOING), 2)
        self.assertEqual(v1.get_number_of_edges(where_to=Vertex.INCOMING), 1)
        self.assertEqual(v1.get_all_connected_nodes(where_to=Vertex.OUTGOING), [v2, v3])
        self.assertEqual(v2.get_number_of_edges(where_to=Vertex.OUTGOING), 0)
        self.assertEqual(v2.get_number_of_edges(where_to=Vertex.INCOMING), 1)
        self.assertEqual(v2.get_all_connected_nodes(where_to=Vertex.INCOMING), [v1])
        self.assertEqual(v3.get_number_of_edges(where_to=Vertex.OUTGOING), 1)
        self.assertEqual(v3.get_number_of_edges(where_to=Vertex.INCOMING), 1)
        self.assertEqual(v3.get_all_connected_nodes(where_to=Vertex.INCOMING), [v1])
        self.assertEqual(v3.get_all_connected_nodes(where_to=Vertex.OUTGOING), [v1])

        # two same methods
        v1.disconnect_node("C")
        # v1.disconnect_node(v3)

        # v2 <- v1 v3

        self.assertEqual(v1.get_number_of_edges(where_to=Vertex.OUTGOING), 1)
        self.assertEqual(v1.get_number_of_edges(where_to=Vertex.INCOMING), 0)
        self.assertEqual(v1.get_all_connected_nodes(where_to=Vertex.OUTGOING), [v2])
        self.assertEqual(v2.get_number_of_edges(where_to=Vertex.OUTGOING), 0)
        self.assertEqual(v2.get_number_of_edges(where_to=Vertex.INCOMING), 1)
        self.assertEqual(v2.get_all_connected_nodes(where_to=Vertex.INCOMING), [v1])
        self.assertEqual(v3.get_number_of_edges(where_to=Vertex.OUTGOING), 0)
        self.assertEqual(v3.get_number_of_edges(where_to=Vertex.INCOMING), 0)
        self.assertEqual(v3.get_all_connected_nodes(where_to=Vertex.INCOMING), [])
        self.assertEqual(v3.get_all_connected_nodes(where_to=Vertex.OUTGOING), [])

        v2.connect_to_node(v1)
        # v2 <=> v1 v3

        v1.disconnect_node(v2, False)

        self.assertEqual(v1.get_number_of_edges(where_to=Vertex.OUTGOING), 0)
        self.assertEqual(v1.get_number_of_edges(where_to=Vertex.INCOMING), 0)
        self.assertEqual(v2.get_number_of_edges(where_to=Vertex.OUTGOING), 1)
        self.assertEqual(v2.get_number_of_edges(where_to=Vertex.INCOMING), 1)

        # Structure is still v2 <=> v1 v3 but from v1 perspective is v2 v1 v3


if __name__ == '__main__':
    unittest.main()
