__author__ = 'Acko'

import os

from graph.graph import Graph
from graph.vertex_and_edge import Vertex
from trie.trie import Trie
from html_parser.html_parser import Parser
from utils.postfix_parser import PostfixParser


class Search(object):
    """ Main class for search.

        When instanced it creates all structures necessary for internal work, and does initial
        database reading and parsing.

        It contains bunch of 'private' methods used for internal operating, and one 'public' method
        which should be used for searching words and syntagms, and one static public method for writing out
        base instructions for users.

        USE:
            s = Search(path_to_database)
            Search.print_instruction()
            s.find_expression(expression)
    """

    def __init__(self, file_path):
        """ Constructor, initialize all of necessary data structures, and loads all data from database in them

            Object has trie - which is used for storing all words and data about word origin, graph which is used
            for path linking (database linking in operative memory), file_list and file_words_list which are side
            lists used for some internal manipulations, and io - (IOAdapter instance) which is used for printing
            out information (results of search)

            Args:
                file_path - path to database (with html files)
        """

        self._trie = Trie()
        self._graph = Graph(directed=True)
        self._file_list, self._file_words_list = [], []
        self._io = Search.IOAdapter(self._file_list, file_path)

        self.__load_data(os.path.abspath(file_path), Parser())

    def __load_data(self, file_path, parser):
        """ Recursion based method, which goes DFS search and parses all html files found

            For each html (htm) file found in database structure, two methods are called, handle_links, and
            handle_words, which then does all work with words found in file and links found in file.

            Args:
                file_path - path to file (folder) which should be read
                parser - Parser instance which is used to parse html files and extract words and links from them
        """

        if os.path.isfile(file_path) and file_path.split(".")[-1] in ['html', 'htm']:
            links, words = parser.parse(file_path)
            self.__handle_links(file_path, links)
            self.__handle_words(file_path, words)
        elif os.path.isdir(file_path):
            for child in os.listdir(file_path):
                self.__load_data(os.path.join(file_path, child), parser)
        return

    def __handle_links(self, file_path, links):
        """ Method which turns given path and links into graph nodes, and binds them into Search graph

            It creates graph_node with file_path as key if it doesn't already exist, and then connects it
            with all links (which also are turned into graph_node new one if it doesn't exists), with outgoing
            edges (which indicates that current file_path node is pointing to other nodes (links)

            Args:
                file_path - path to file from which are read links
                links -  links on which currently read file pointing
        """

        file_path = os.path.abspath(file_path)
        if self._graph.get_node(file_path) is None:
            self._graph.create_node(file_path)
        for link in links:
            link = os.path.abspath(link)
            if self._graph.get_node(link) is None:
                self._graph.create_node(link)
            self._graph.connect_nodes(self._graph.get_node(file_path), self._graph.get_node(link))

    def __handle_words(self, file_path, words):
        """ Method which stores all words into trie and sets its origin with some additional data

            First it appends file_path graph node to Search file_list and number of words from that path
            into Search file_words_list. Then it adds each word into trie and sets last character additional data
            to dictionary, in which then adds file_path (index from file_list) as a key and list of indexes
            where word is found as a value (used later in syntax search)

            Args:
                file_path - path to file from which are read words
                words - list of all words from file (at given file_path)
        """

        self._file_list.append(self._graph[file_path])
        self._file_words_list.append(len(words))
        for index, word in enumerate(words):
            # time_h = datetime.datetime.now()
            # self._trie.has_word(word)                               # 00:12.5
            # Utils.sum8 += datetime.datetime.now() - time_h
            # if not self._trie.has_word(word):
            #     time_hh = datetime.datetime.now()
            #     self._trie.add_word(word)                           # 00:01.36
            #     Utils.sum5 += datetime.datetime.now() - time_hh
            #     time_hh = datetime.datetime.now()
            #     self._trie.get_node(word).set_data({})              # 00:00.4
            #     Utils.sum6 += datetime.datetime.now() - time_hh
            #
            # if self._trie.get_node(word).get_data().get(file_path) is None:
            # time_l = datetime.datetime.now()
            # self._trie.get_node(word).get_data()[len(self._file_list) - 1] = c[word]  # 00:13.3
            # Utils.sum7 += datetime.datetime.now() - time_l

            node = self._trie.add_word(word)
            if node.get_data() is None:
                node.set_data({})
            try:
                node.get_data()[len(self._file_list) - 1].append(index)
            except KeyError:
                node.get_data()[len(self._file_list) - 1] = [index]

    def __search_word(self, word, words):
        """ Method which finds given word in Search trie

            Args:
                word - (string) which should be looked for
                words - (dict) dictionary in which will all results be putted

            Return:
                Dictionary set as additional data for given word in trie if such word exists, or
                empty dictionary if it doesn't
        """

        res_node = self._trie.get_node(word).get_data() if self._trie.get_node(word) is not None else {}
        words[word] = res_node if res_node is not None else {}
        return res_node if res_node is not None else {}

    def __search_syntagm(self, key, words_, escape_sequence):
        """ Method for searching syntagms.

            First it gets syntagm for search from escape_sequence dictionary, then creates list of words files
            which contains all of those words, and then for each file (which contains all words) it goes through
            list of word results, and checks if there is any index series, where each next word has index + 1

            When ever found such series, number of showing up times raises by one, and current file index is
            added to final_list dictionary (which will be returned). Also words dictionary is with key as key
            and final_list as value.

            Args:
                key - escape key found (recognizes) for which there is an syntax
                words_ - dictionary which should be filled with results for given key
                escape_sequence - dictionary with syntagms which are hidden by key

            Return:
                final_list (dict) which contains all files where syntagm is found as keys, and
                how many times it shows up as value
        """

        words = escape_sequence[key[1:]].split()
        res_list = self.find_expression(escape_sequence[key[1:]], True)
        final_list = {}
        word_list = []
        for word in words:
            word_list.append(self.__search_word(word, words_))

        for index, element in enumerate(res_list):
            indexes = {}
            for index2, word_res_list in enumerate(word_list):
                try:
                    indexes[index2] = word_list[index2][element]
                except KeyError:
                    indexes[index2] = []
            add_const, show_up = 1, 0
            bool_flag = True
            for index2 in indexes[0]:
                bool_flag = True
                while add_const < len(words):
                    if index2 + add_const in indexes[add_const]:
                        add_const += 1
                    else:
                        bool_flag = False
                        break
                if bool_flag:
                    show_up += 1
            if bool_flag:
                final_list[element] = show_up

        words_[key] = final_list
        return final_list

    def find_expression(self, expression, side=False):
        """ Method which should be used (only) from outside. It finds expression and prints out results

            First it creates all necessary dictionaries (which are used by other methods), and using PostfixParser
            parses expression into postfix list. Then for each element calls either search_word or search_syntagm
            depending on element type, and those search results sets into new postfix list, which then passes
            to PostfixParser calculate_postfix (LIST) to get final results.

            In the end it sends those results to sort method which sorts it by priority and calls printing method.

            Args:
                expression - expression to be found
                side - (bool) flag which indicates if results should be printed or just returned

            Return:
                final result list (passed to sort method if side is False)

            Raise:
                Nothing by it self, but other methods called from here can raise:
                InvalidInput - if expression can not be parsed
                QuitRequested - if QUIT exception found
        """

        escape_sequences, words = {}, {}
        postfix_list = PostfixParser.convert_postfix(expression, escape_sequences)
        side_list = []

        for el in postfix_list:
            side_list.append(el)

        for index, element in enumerate(side_list):
            if element not in PostfixParser.OPERATORS.keys():
                if element.startswith(PostfixParser.KEY_SIGN):
                    side_list[index] = self.__search_syntagm(element, words, escape_sequences).keys()
                else:
                    side_list[index] = self.__search_word(element, words).keys()

        final_list = PostfixParser.calculate_postfix_list(side_list, range(len(self._file_list)))

        if side:
            return final_list

        return self.__sort_result(final_list, postfix_list, words)

    def __sort_result(self, final_list, postfix_list, words):
        """ Sorting method, sorts list of results, and sends it to printing method, so it can be printed out.

            It calls method calculate_page_priority which calculates priority for each one file (path) from
            given final_list, and postfix_list, and then, sorts final list using those values as comparison
            parameters. (It uses built in sort method)

            In the end it calls IOAdapter method for printing out results.

            Args:
                final_list - list get by find_expression method, which contains list of all files which
                        fit in search request
                postfix_list - token list in postfix order, used in calculate_page_priority
                words -  list of all words and syntagms search results, so that when calculating priorities
                        it doesn't have to search them again
        """

        priority_list = self.__calculate_page_priority(final_list, postfix_list, words)
        final_list.sort(key=lambda item: priority_list[item], reverse=True)
        self._io.print_results(final_list, priority_list)

    def __calculate_page_priority(self, final_list, postfix_list, words):
        """ Method which calculates each element from final_list summed priority

            It calculates page priority based on three parameters, word count in given file, number of links
            which points to given file, and word count in those links. It uses 1 : 0.7 : 0.4 ratio.

            It uses calculate_word_priority method to get word count (which follows logic in expression)

            Args:
                final_list - list of all files which fit search result
                postfix_list - token list in postfix order (needed for calculate_word_count)
                words - dictionary which contains all search results for all words so that word count
                        doesn't have to be calculated again

            Return:
                Dictionary whit all files from final_list as keys and theirs priority as values
        """

        priority_list = {}

        for index in final_list:
            given_file, number_of_links, other_files = 0, 0, 0

            given_file = self.__calculate_word_priority(postfix_list, self._file_list[index], words)

            number_of_links = self._file_list[index].get_number_of_edges(where_to=Vertex.INCOMING)

            for node in self._file_list[index].get_all_connected_nodes(where_to=Vertex.INCOMING):
                other_files += self.__calculate_word_priority(postfix_list, node, words)

            priority_list[index] = given_file + 0.7 * number_of_links + 0.4 * other_files

        return priority_list

    def __calculate_word_priority(self, postfix_list, graph_node, words):
        """ Method for calculating word count priority part, following expression logic

            It goes through postfix_list and creates new one by changing all words with their count
            (based on words dictionary) which is then passed to PostfixParser calculate_postfix (INT) method,
            which then returns number (presenting current page word count priority)

            Args:
                postfix_list - token list in postfix order
                graph_node - Graph node form Search file_list for which words should be calculated
                words - dictionary which contains all word search results, so that it doesn't have to be calculated
                        again

            Return:
                Number which presents word count part of priority for given node
        """

        side_list = []
        for el in postfix_list:
            side_list.append(el)

        for i, el in enumerate(side_list):
            if el not in PostfixParser.OPERATORS.keys():
                try:
                    if side_list[i].startswith(PostfixParser.KEY_SIGN):
                        side_list[i] = words[self._file_list.index(graph_node)][side_list[i]]
                    else:
                        side_list[i] = len(words[el])
                # KeyError - if word is in trie but doesn't show in current node (path)
                # AttributeError - if word is not in trie at all
                except (KeyError, AttributeError):
                    side_list[i] = 0
        return PostfixParser.calculate_postfix_list(side_list, self._file_words_list[self._file_list.index(graph_node)],
                                                    PostfixParser.INT)

    @staticmethod
    def print_instruction():
        """ Static method for printing out instructions so that user knows how to use this class """

        Search.IOAdapter.print_instruction()

    class IOAdapter(object):
        """ Inner Class which is used to be output stream adapter for Search class

            When instanced it gets file_list which it uses to decode list of results which should be printed out,
            and file_path which is path user typed in, which it uses for parsing abspath so that output looks better.

            It shouldn't be used from outside, it is just inside Search class
        """

        def __init__(self, file_list, file_path):
            """ Constructor which sets given attributes as instance attributes

                Args:
                    file_list - list which is used for mapping results with Vertex instances
                    file_path - path typed in by user (which shouldn't be printed out)
            """
            self._file_path = file_path
            self._file_list = file_list

        def print_results(self, final_list, priority_dictionary):
            """ Method which prints out results with their priorities

                Args:
                    final_list - list of indexes (which presents files) which should be printed
                    priority_dictionary - dictionary which maps indexes with their priority
            """
            print
            print "Rezultati pretrage: "
            Search.IOAdapter._print_break()

            if len(final_list) == 0:
                print "Za unete reci ne postoje rezultati."
            else:
                for index, result in enumerate(final_list):
                    print str(index + 1) + ") " + "%-40s | %8d |" % (
                        os.path.relpath(self._file_list[result].get_key(), self._file_path),
                        priority_dictionary[result])

            Search.IOAdapter._print_break()
            print

        @staticmethod
        def print_instruction():
            """ Static method which prints out instruction (hard coded) """

            print '\nUputstvo za upotrebu: '
            print 'Unosenjem vise od jedne reci razdvojene razmakom (ili skupom razmaka) dobicete'
            print 'skup fajlova u kojima se nalaze sve reci.\n'
            print 'Kljucne reci za logicke operature su "AND", "OR" i "NOT" (ili "&", "|", "!").'
            print '"NOT" operator se posmatra kao unarni operator najviseg prioriteta, dok su "AND"'
            print 'i "OR" binarni operatori nizeg prioriteta ("AND" > "OR").\n'
            print 'Za pretrazivanje sintagmi, zeljenu sintagmu zapisite pod navodnicima.\n'

        @staticmethod
        def _print_break():
            """ Static method which prints break line (100 times '*') """

            print '*' * 100