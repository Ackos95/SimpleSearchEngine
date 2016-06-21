"""
    Module contains two classes, Vertex, and Edge, which presents two side classes for graph
"""

__author__ = 'Acko'


class Vertex(object):
    """ Class which represents one Vertex in Graph

        It contains two static final attributes (used as parameters in some methods)
        _key - which is something that declares one Vertex
        _data -  additional data which can be bound to Vertex instance
        _directed - (bool) flag which describes if graph is directed or not
        and two lists _outgoing and _incoming, which are two different lists if graph is
        directed, otherwise are two reference to same list. They contain list of all edges
        with which current Vertex is bound.
    """

    # CONSTANTS
    OUTGOING, INCOMING = 1, 2
    __slots__ = ['_key', '_data', '_directed', '_outgoing', '_incoming']

    def __init__(self, key, data=None, directed=False):
        """ Constructor, sets initial parameters of Vertex

            Args:
                key - key which represents one Vertex
                data - (initially None) additional data which can be bound to Vertex
                directed - (bool, initially False) flag which describes if Vertex is directed
        """

        self._key = key
        self._data = data
        self._directed = directed
        self._outgoing = []
        self._incoming = [] if directed else self._outgoing

    def get_key(self):
        """ Getter method for current Vertex key

            Return:
                key of current Vertex instance
        """

        return self._key

    def has_data(self):
        """ Method which determines if any additional data is bound to Vertex

            Return:
                True if any data is bound to current Vertex, False otherwise
        """

        return self._data is not None

    def get_data(self):
        """ Getter method for data bound to current Vertex instance

            Return:
                data (object) which is bound to current Vertex, or None if there is no data bound
        """

        return self._data

    def set_data(self, data):
        """ Setter method for data field

            Args:
                data - (object) data which will be bound with (to) Vertex
        """

        self._data = data

    def is_directed(self):
        """ Method with which is determined if current Vertex is directed or not

            Return:
                True if vertex is directed, False otherwise
        """

        return self._directed

    def add_link(self, link, where_to=OUTGOING):
        """ Method for adding new link between current vertex, and one more (which should be in link).

            It can bind it as outgoing link, or as incoming, which only make sense when vertex is directed,
            it also checks link if it is valid, and then binds it all together.

            Args:
                link - (Edge instance) which should connect current vertex, with another one
                where_to - (Vertex constant) flag which indicates how link should be added

            Raise:
                TypeError - if link is not Edge instance
                Exception -  if parameters doesn't match, or given node is already connected
        """

        if not isinstance(link, Edge):
            raise TypeError("Link must be edge instance")

        if where_to == Vertex.OUTGOING:
            if not link.get_start_vertex() is self:
                raise Exception("Wrong Link connecting")

            if link.get_end_vertex() in self.get_all_connected_nodes():
                raise Exception("Already connected")

            self._outgoing.append(link)

        elif where_to == Vertex.INCOMING:
            if not link.get_end_vertex() is self:
                raise Exception("Wrong Link connecting")

            if link.get_start_vertex() in self.get_all_connected_nodes(where_to=Vertex.INCOMING):
                raise Exception("Already connected")

            self._incoming.append(link)

    def connect_to_node(self, vertex, where_to=OUTGOING):
        """ Method which connects current vertex to another vertex passed as parameter

            It creates Edge instance (with appropriate parameters (self, vertex)) and then adds it
            to current vertex list and another vertex list (also depending on parameter and direction)

            Args:
                vertex - (Vertex instance) another vertex which should be bound with current one
                where_to - (Vertex constant) constant which describes if another vertex should be added
                        with outgoing link or incoming link

            Raise:
                TypeError - if vertex is not Vertex instance
        """

        if not isinstance(vertex, Vertex):
            raise TypeError("Graph vertex can only connect to other Graph vertex")

        if where_to == Vertex.OUTGOING:
            link = Edge(self, vertex)
            self.add_link(link, Vertex.OUTGOING)
            vertex.add_link(link, Vertex.INCOMING)

        elif where_to == Vertex.INCOMING:
            link = Edge(vertex, self)
            self.add_link(link, Vertex.INCOMING)
            vertex.add_link(link, Vertex.OUTGOING)

    def get_number_of_edges(self, where_to=OUTGOING):
        """ Method which returns exact number of edges for current Vertex

            Args:
                where_to - (Vertex constant) describes if is asked for number of outgoing or incoming edges

            Return:
                Number of edges which current vertex contains
        """

        if not self._directed:
            return len(self._outgoing)

        if where_to == Vertex.OUTGOING:
            return len(self._outgoing)
        elif where_to == Vertex.INCOMING:
            return len(self._incoming)

    def get_all_edges(self, where_to=OUTGOING):
        """ Method for retrieving list of all edges with which current vertex is bound to other vertexes

            Args:
                where_to - (Vertex constant) describes if should be returned list of all outgoing or incoming edges

            Return:
                List of all edges with which current vertex is bound to other vertexes
        """

        if where_to == Vertex.OUTGOING:
            return self._outgoing
        elif where_to == Vertex.INCOMING:
            return self._incoming

    def get_edge(self, vertex, where_to=OUTGOING):
        """ Method for retrieving exact edge which connects current vertex with one passed as parameter, if such exists

            Args:
                vertex - (Vertex instance) with which link is searched for
                where_to - (Vertex constant) describes if link should be searched for in outgoing or incoming links

            Return:
                Edge instance which binds this two vertexes, if such exists, None if not
        """

        edge_list = None

        if where_to == Vertex.OUTGOING:
            edge_list = self._outgoing

        elif where_to == Vertex.INCOMING:
            edge_list = self._incoming

        for edge in edge_list:
            if edge.return_other_side(self) is vertex:
                return edge
        return None

    def get_all_connected_nodes(self, where_to=OUTGOING):
        """ Method which returns list of all vertexes which are bound to current one

            Args:
                where_to - (Vertex constant) describes if should be returned list of all incoming
                        or outgoing linked vertexes

            Return:
                list of all vertexes which are bound to current vertex (incoming or outgoing depends on parameter)
        """

        list_of_all_nodes = []

        if not self._directed or where_to == Vertex.OUTGOING:
            for edge in self._outgoing:
                list_of_all_nodes.append(edge.return_other_side(self))
        elif where_to == Vertex.INCOMING:
            for edge in self._incoming:
                list_of_all_nodes.append(edge.return_other_side(self))

        return list_of_all_nodes

    def disconnect_node(self, vertex, true=True):
        """ Method for removing node from connected nodes (works both ways)

            First it checks if passed vertex is Vertex instance, if not raises error, then
            checks if given vertex exists in connected nodes lists, also if it is not raises error.
            Then looks for edge which connects two nodes, and when it founds it, saves index and delete edge
            from edge list. (If node is directed, it goes through list of incoming, if not just through
            outgoing list - because it is same list if node is not directed).

            And in the end, calls itself if true parameter is set on True for given vertex (assuming that nodes are
            connected by default method, and that both nodes have reference to edge which connects them)
            so that connection gets destroyed in both sides

            Args:
                vertex - (Vertex instance or key) vertex (or key to vertex) which should be disconnected
                true - (bool) which describes if disconnection will be both ways
        """

        if not isinstance(vertex, Vertex):
            for node in self.get_all_connected_nodes(where_to=Vertex.OUTGOING):
                if node.get_key() == vertex:
                    vertex = node
                    break
            if not isinstance(vertex, Vertex):
                for node in self.get_all_connected_nodes(where_to=Vertex.INCOMING):
                    if node.get_key() == vertex:
                        vertex = node
                        break
            if not isinstance(vertex, Vertex):
                raise KeyError("Vertex with given key not found in connected nodes")

        else:
            if vertex not in self.get_all_connected_nodes(where_to=Vertex.OUTGOING)\
                    and vertex not in self.get_all_connected_nodes(where_to=Vertex.INCOMING):
                raise KeyError("Vertex not found in connected nodes")

        out_index = None
        for edge in self._outgoing:
            if edge.return_other_side(self) is vertex:
                out_index = self._outgoing.index(edge)

        if out_index is not None:
            self._outgoing.pop(out_index)

        if self._directed:
            in_index = None
            for edge in self._incoming:
                if edge.return_other_side(self) is vertex:
                    in_index = self._incoming.index(edge)

            if in_index is not None:
                self._incoming.pop(in_index)

        if true:
            try:
                vertex.disconnect_node(self)
            except KeyError:
                return

    def __hash__(self):
        """ Overriding hash method """

        return hash(id(self))


class Edge(object):
    """ Class which represents link (bind) between two graph nodes (vertexes)

        It contains start_vertex, vertex which is at beginning of link, and end_vertex
        which is at end of link. And also it contains one field _data which is place for
        additional data which can be bound together with Edge instance
    """

    def __init__(self, start_vertex, end_vertex, data=None):
        """ Constructor, sets initial attributes of Edge instance

            Args:
                start_vertex - (Vertex instance) vertex which is placed at beginning of link
                end_vertex - (Vertex instance) vertex which is placed at end of link
                data - (object) initially None, additional data which could be bound to Edge instance

            Raise:
                TypeError - if start_vertex or end_vertex does not match format (not Vertex instances)
        """

        if not isinstance(start_vertex, Vertex) or not isinstance(end_vertex, Vertex):
            raise TypeError("Edge can connect only Vertex instances")

        self._start_vertex = start_vertex
        self._end_vertex = end_vertex
        self._data = data

    def get_start_vertex(self):
        """ Getter method for start_vertex, returns reference to Vertex instance which is at beginning of link

            Return:
                Reference to Vertex instance which is placed at beginning of link
        """

        return self._start_vertex

    def get_end_vertex(self):
        """ Getter method for end_vertex, returns reference to Vertex instance which is at end of link

            Return:
                Reference to Vertex instance which is placed at end of link
        """

        return self._end_vertex

    def has_data(self):
        """ Method for establishing if any additional data is bound to current Edge (link)

            Return:
                True if any data is bound to Edge, False otherwise
        """

        return self._data is not None

    def get_data(self):
        """ Getter method for data field

            Return:
                Data (object) which is bound to current Edge, if there is any, None otherwise
        """

        return self._data

    def set_data(self, data):
        """ Setter method for data field

            Args:
                data - (object) object which will be bound to current Edge as additional data
        """

        self._data = data

    def return_other_side(self, vertex):
        """ Method which returns vertex which is placed on other side from vertex passed as parameter

            Args:
                vertex - (Vertex instance) whose other side is looked for, must be bound to current Edge
                        or else TypeError will be raised

            Return:
                Vertex instance at other side of current edge

            Raise:
                TypeError - if vertex passed as parameter is not bound to current Edge
        """

        if vertex is not self._start_vertex and vertex is not self._end_vertex:
            raise TypeError("Wrong call")

        if vertex is self._start_vertex:
            return self._end_vertex
        elif vertex is self._end_vertex:
            return self._start_vertex