__author__ = 'Acko'

from vertex_and_edge import Vertex


class Graph(object):
    """ Main graph structure, it contains map of nodes, and flag which indicates if Graph is directed

        It contains some basic methods for handling Vertex instance creating, and connecting, with some Edge instances.
        Basically it is meant to be Handler for Vertex (Edge) using
    """

    def __init__(self, directed=False):
        """ Constructor, sets initial parameters of instance

            Args:
                directed - (bool) flag which describes if Graph is directed (is Vertex nodes going to be directed)
        """

        self._nodes = {}
        self._directed = directed

    def _add_node(self, node):
        """ Method for adding node into structure.

            It is protected, because it is meant to be used implicitly by using create_node method.
            Just checks if node passed is Vertex instance, and if not raises TypeError

            Args:
                node - (Vertex instance) which should be added to Graph structure

            Raise:
                TypeError - if passed node is not Vertex instance
        """

        if not isinstance(node, Vertex):
            raise TypeError("Node must be vertex")

        self._nodes[node.get_key()] = node

    def create_node(self, key, data=None):
        """ Method for creating new Vertex instance and putting it inside Graph structure

            This method is meant to be used from outside class, because it checks if node with same key
            already exists in Graph, and if not it creates new Vertex with given data, and puts it into structure

            Args:
                key - (object) should be unique key which represent Vertex instance
                data -  (object) represents object spot for additional data which can be bound to Vertex instance

            Raise:
                Exception - if Vertex with same key already exists in Graph instance
        """

        if self.exists(key):
            raise Exception("Vertex with same key already exists in graph")

        v = Vertex(key, data, self._directed)
        self._add_node(v)

    def exists(self, key):
        """ Method for checking if node with given key exists in graph instance

            Args:
                key - Unique representation of Vertex instance which is looked for in Graph instance

            Return:
                True if Graph contains node with given key, False otherwise
        """

        return self._nodes.get(key) is not None

    def connect_nodes(self, first, second):
        """ Method for connecting two nodes (which should already be in graph)

            It checks if passed parameters are Vertex instances, if not error is raised, then
            checks if both of instances are already in graph, if not error is raised, and finally
            when all checks are passed, then two nodes are connected

            Args:
                first - (Vertex instance) starting point of connection
                second - (Vertex instance) ending point of connection

            Raise:
                TypeError - if parameters are not Vertex instances
                Exception - if Vertexes don't exist in Graph instances
        """

        if not isinstance(first, Vertex) or not isinstance(second, Vertex):
            raise TypeError("Wrong parameter types, must be vertex")

        if not self.exists(first.get_key()) or not self.exists(second.get_key()):
            raise Exception("One of vertexes which are you trying to connect is not in Graph")

        first.connect_to_node(second, where_to=Vertex.OUTGOING)

    def connect_both_ways(self, first, second):
        """ Method for connecting two nodes both ways (<=>)

            It relies on connect_nodes method which does all checks and raises error if anything
            goes wrong

            Args:
                first - (Vertex instance) node to be connected
                second - (Vertex instance) node to be connected
        """

        self.connect_nodes(first, second)
        self.connect_nodes(second, first)

    def remove_node(self, vertex):
        """ Method for removing vertex from Graph instance

            It checks for vertex in graph, if vertex is not in graph, it raises error,
            Then, it disconnect vertex from all Vertexes which are in graph, and finally
            deletes vertex from Graph's vertex dictionary

            Args:
                vertex - (Vertex instance, or key to vertex)

            Raise:
                KeyError -  if vertex was not found in graph
        """

        if not isinstance(vertex, Vertex):
            if self.get_node(vertex) is None:
                raise KeyError("Vertex with given key doesn't exists in graph")
            vertex = self.get_node(vertex)

        copy_list = []
        for node in vertex.get_all_connected_nodes(where_to=Vertex.OUTGOING):
            copy_list.append(node)

        for node in copy_list:
            if self.get_node(node.get_key()) is not None:
                vertex.disconnect_node(node)  # will disconnect both ways

        if self.is_directed():
            copy_list = []
            for node in vertex.get_all_connected_nodes(where_to=Vertex.INCOMING):
                copy_list.append(node)

            for node in copy_list:
                if self.get_node(node.get_key()) is not None:
                    vertex.disconnect_node(node)  # will disconnect both ways

        del self._nodes[vertex.get_key()]

    def is_directed(self):
        """ Method for checking if Graph is directed or not

            Return:
                True if graph is directed, False otherwise
        """

        return self._directed

    def get_all_nodes(self):
        """ Method which returns list of all Vertex instances which are in Graph

            Return:
                List of all Vertex instances which are in graph
        """

        return self._nodes.values()

    def get_node(self, key):
        """ Method for getting Vertex instance by it's key. Works for vertexes which are in graph

            Args:
                key - unique representation of Vertex instance which is looked for in graph

            Return:
                Vertex instance with given key (if exists in Graph) or None (if it doesn't)
        """

        return self._nodes.get(key)

    def __getitem__(self, item):
        """ Method for getting instance in dictionary style ( graph [item] )

            Args:
                item - key which will be passed to get_node method

            Raises:
                KeyError - if doesn't exist Vertex with given key in graph
        """

        if self.exists(item):
            return self._nodes.get(item)
        raise KeyError("Vertex with given key doesn't exist in graph")