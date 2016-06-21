__author__ = 'Acko'

import datetime


class TrieNode(object):
    """ Class which represents one node of Trie structure

        It contains key - which should be letter, data - which is usually empty (unless you need it for something)
        end - (bool) flag which represents if this node represents end of sentence (usually  word)
        parent - (TrieNode) which presents parent node, just reference to the parent and
        child_list - (list of TrieNodes) which presents all of TrieNodes which are children of current node
    """

    __slots__ = ['_key', '_data', '_end', '_parent', '_child_list']

    def __init__(self, key, parent=None, data=None, end=False):
        """  Constructor, sets initial data for instance

            Args:
                key - (String - char) should be letter (should represent a node in higher structure)
                parent - (TrieNode) reference to parent of current node
                data - (object) can be anything, whatever you need to store inside one node
                end - (bool) flag which represents if concrete node is end of sentence (word usually)

            Raise:
                TypeError - if key or parent doesn't match supported types
        """
        if not isinstance(key, str):
            raise TypeError("Key must be string")

        if not isinstance(parent, TrieNode) and parent is not None:
            raise TypeError("Parent must be TrieNode instance or None")

        self._key = key
        self._data = data
        self._end = end
        self._parent = parent
        self._child_list = {}

        if parent is not None:
            parent.insert_child(self)

    def is_end(self):
        """ Method which tells us if current node is End of sentence (word usually)

            Return:
                True if it is end, False otherwise
        """

        return self._end

    def get_key(self):
        """ Getter method for key attribute of current node

            Return:
                Current node's key (String - char)
        """

        return self._key

    def get_data(self):
        """  Getter method for data attribute of current node

            Return:
                Current node's data (object)
        """

        return self._data

    def get_parent(self):
        """ Getter method for current node's parent reference

            Return:
                Current node's parent (TrieNode)
        """

        return self._parent

    def get_child_list(self):
        """ Getter method for current node's child_list

            Return:
                Current node's child_list (dict: key - child's key, value - child (TrieNode))
        """

        return self._child_list

    def insert_child(self, child):
        """ Method for inserting new child into current node's child_list

            Args:
                child - (TrieNode) instance which should be added in child_list

            Return:
                child instance added into current node's child_list (TrieNode)

            Raise:
                Exception: if child passed is not TrieNode instance
        """

        if not isinstance(child, TrieNode):
            raise Exception("Child must be TrieNode")

        if not self._child_list.get(child.get_key()):
            self._child_list[child.get_key()] = child
        return self._child_list[child.get_key()]

    def has_child(self, key):
        """ Method which is used to check if current node has a child with given key

            Args:
                key - (String - char) that should be looked for in child_list (TrieNode keys)

            Return:
                True if child with given key exists, False otherwise
        """

        try:
            self._child_list[key]
            return True
        except KeyError:
            return False

    def get_child(self, key):
        """ Method which returns child (TrieNode) instance which is in current child_list at given key

            Args:
                key - (String - char) of a child that should be found and returned from current node's child_list

            Return:
                Child at given position (TrieNode) if exists, None otherwise
        """

        try:
            return self._child_list[key]
        except KeyError:
            return None

    def has_data(self):
        """ Method for checking if current node has some additional data stored in its data section

            Return:
                True if current node has some data stored, False otherwise
        """

        return self._data is not None

    def set_end(self):
        """ Sets end flag of current node to True, which indicates that current node is end of sentence """

        self._end = True

    def set_data(self, data):
        """ Setter method for data, it sets any object into _data field of TrieNode instance

            Args:
                data - (object) which goes into current node's _data field

        """

        self._data = data

    def __str__(self):
        """ String representation of one TrieNode instance

            Return:
                String representation of one node instance (its key)
        """

        return self._key

    def __getitem__(self, item):
        """ Getitem method (built in). Simulates dictionary behave (TrieNode[item])

            Args:
                item - key with which should

            Return:
                child (TrieNode) with given key if exists

            Raise:
                KeyError if child with given key doesn't exist
        """

        if self.has_child(item):
            return self._child_list[item]
        raise KeyError("No such key")


class Trie(object):
    """ Simple class which is used as a container for TrieNode instances

        When instanced it sets initial root node as root, with special key (__root__)
        It has two simple methods one for adding words into tree, and one for checking
        if given word is in tree. Both methods contain (default true) flag for ignore case
        mode.
    """

    current_time = datetime.timedelta()
    is_end = datetime.timedelta()
    has_child = datetime.timedelta()
    ignore_case = datetime.timedelta()
    current_change = datetime.timedelta()

    def __init__(self):
        """ Constructor, sets root node of tree """

        self._root = TrieNode('__root__')

    def add_word(self, word, ignore_case=True):
        """ Method for adding new word into trie, word must be string type

            Args:
                word - (String) which is parsed into letters and each letter then added
                    into the TrieNode which is then bound into tree
                ignore_case - (bool) flag which indicates if word should be added small_cased
                    or as is, if it is True word is added small_cased, otherwise as is
                    Default value is True
        """

        current = self._root
        for letter in word:
            if ignore_case:
                letter = letter.lower()
            if not current.has_child(letter):
                child = TrieNode(letter, current)
                current.insert_child(child)
            current = current.get_child(letter)

        current.set_end()
        return current

    def has_word(self, word, ignore_case=True):
        """ Checks if given word is in tree or not

            Args:
                word - (String) which should be looked for in tree
                ignore_case - (bool) flag which indicates if word should be looked for
                    small_cased or as entered. If set on True it will be looked for small_cased
                    otherwise as is. Default value is True

            Return:
                True if word is in tree, False otherwise
        """

        # time = datetime.datetime.now()
        current = self._root
        # Trie.current_time += datetime.datetime.now() - time
        if ignore_case:
            word = word.lower()

        for letter in word:
            # time = datetime.datetime.now()
            # current.has_child(letter)
            # Trie.has_child += datetime.datetime.now() - time
            # time = datetime.datetime.now()
            # Trie.ignore_case += datetime.datetime.now() - time
            if not current.has_child(letter):
                return False
            # time = datetime.datetime.now()
            current = current.get_child(letter)
            # Trie.current_change += datetime.datetime.now() - time

        # time = datetime.datetime.now()
        # current.is_end()
        # Trie.is_end += datetime.datetime.now() - time
        if not current.is_end():
            return False

        return True

    def get_node(self, word, ignore_case=True):
        """ Method for getting TrieNode instance which is placed at last character (in word passed)

            Method will find any TrieNode if exists, it doesn't have to be word ending (like in has_word method)

            Args:
                word - (String) which end character will be looked for in trie and returned its node
                ignore_case - (bool) flag which indicates if word should be looked for
                    small_cased or as entered. If set on True it will be looked for small_cased
                    otherwise as is. Default value is True

            Return:
                TrieNode instance which is placed at last character in word passed, or None if word not found
        """

        current = self._root
        if ignore_case:
            word = word.lower()

        for letter in word:
            if not current.has_child(letter):
                return None
            current = current.get_child(letter)

        return current