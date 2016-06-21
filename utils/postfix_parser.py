__author__ = 'Acko'

import re
import itertools

from stack import Stack


class QuitRequest(Exception):
    """ Exception class """
    pass


class InvalidInput(Exception):
    """ Exception class """
    pass


class PostfixParser(object):
    """ Container class which contains all static methods for parsing inputs, and doing some calculations with results

        It contains bunch of 'private' methods for internal work, and two 'public methods' for users outside.
        Use of this class is to parse given expression, check its validity and turns it into postfix list of words
        and operators. It goes through expression, switch all key words with appropriate special signs, then
        checks validity, and converts it to postfix.

        Calculate postfix need some outside work, postfix list given to it should contain lists which should be
        operated on, or integers (which should be operated on).

        Use:
            postfix_list = PostfixParser.convert_postfix(expression, escape_sequence) and
            res_list (or priority) = PostfixParser.calculate_postfix(set_up_postfix_list, whole_list, LIST (or INT))
    """

    # CONSTANTS
    LIST, INT = 1, 2
    KEY_SIGN = '$'

    # Two dictionaries with some methods (lambda functions) bound to keys of operations
    LIST_METHODS = {'&': lambda list_a, list_b: [x for x in list_a if x in list_b],
                    '|': lambda list_a, list_b: [value for row in itertools.izip_longest([x for x in list_a],
                                                                                         [y for y in list_b
                                                                                          if y not in list_a])
                                                 if row is not None
                                                 for value in row if value is not None],
                    '!': lambda list_a, list_b: [x for x in list_b if x not in list_a]}
    INT_METHODS = {'&': lambda x, y: max(x - y, y - x), '|': lambda x, y: x + y, '!': lambda x, y: y - x}

    # MORE CONSTANTS (which should be changed if user-interface changes)
    QUIT_ESCAPE = 'QUIT'
    KEY_WORDS = {'AND': '&', 'OR': '|', 'NOT': '!', KEY_SIGN: ''}

    # Operators with priority, and list of all unary operators
    UNARY = ['!']
    OPERATORS = {'&': 5, '|': 1, '!': 10, '(': 100, ')': 100}

    # Regex for parsing expression
    split_param = r'([&|!()])'

    @staticmethod
    def __validate_expression(expression, escape_sequences):
        """ Method which does initial expression split, and validation

            First checks if empty string is entered, then goes through string and switch all key words
            with appropriate special sign, then checks for QUIT key word, if its found QUIT signal is sent,
            Then goes through expression looking for syntagms (by looking for '"' pair) and switch all syntagms
            with dynamically creating keys (which is stored int escape_sequences dictionary).

            After those checks, goes through expression and adds implied '&' signs where words are separated with
            whitespaces. And in the end returns split list with all tokens (words, operators and syntagm keys)

            Args:
                expression -  expression to be evaluated and parsed
                escape_sequence - (dict) dictionary which should be filled with 'key' -> 'syntagm' for all
                        syntagms found inside expression

            Return:
                List of tokens (words, operators and syntagms keys) if expression passes validation, or raises error
                if validation is failed

            Raise:
                InvalidInput - if Validation fails in any moment
                QuitRequest - if 'QUIT' keyword was found inside expression
        """

        if expression.strip() == '':
            raise InvalidInput("Empty string entered.")

        for key_word in PostfixParser.KEY_WORDS.keys():
            expression = expression.replace(key_word, PostfixParser.KEY_WORDS[key_word])

        if PostfixParser.QUIT_ESCAPE in expression:
            raise QuitRequest()

        expression = PostfixParser.__switch_syntagms(expression,
                                                     PostfixParser.__find_syntagms(expression), escape_sequences)

        if '&' not in expression and '|' not in expression and '!' not in expression:
            side_list = expression.split()
            expression = '&'.join(side_list)

        index_list = []
        side_list = expression.split()
        for index, element in enumerate(side_list):
            if element not in PostfixParser.OPERATORS.keys() and index < len(side_list) - 1 \
                    and side_list[index + 1] not in PostfixParser.OPERATORS.keys():
                index_list.append(index + 1)

        adding_const = 0
        for index in index_list:
            side_list.insert(index + adding_const, '&')
            adding_const += 1

        expression = ''.join(side_list)

        return re.split(PostfixParser.split_param, expression.replace(' ', ''))

    @staticmethod
    def __find_syntagms(expression):
        """ Method which goes through expression and finds and replaces all syntagms in it with new key

            It goes through expression, and looks for '"' signs, tries to find starting '"' sing, and ending '"' sign,
            if anything there fails, it raises error (checks for unequal number of '"' signs). Saves all indexes
            of '"' signs (starting and ending in one tuple) and returns it

            Args:
                expression - expression in which should be found all syntagms ('" some random text "')

            Return:
                List of tuples with all '"' showing (tuple (start_sign_index, end_sign_index)) if number of signs
                is correct

            Raise:
                InvalidInput - if number of sings isn't correct
        """

        replace_list = []
        start_const = 0
        start_index, end_index = 0, 0
        while True:
            try:
                start_index = expression.index('"', start_const)
                if start_index - 1 != -1 and expression[start_index - 1] != ' ':
                    raise InvalidInput("Not correctly separated words and syntagms")
                end_index = expression.index('"', start_index + 1)
                if end_index + 1 < len(expression) and expression[end_index + 1] != ' ':
                    raise InvalidInput("Not correctly separated words and syntagms")
                start_const = end_index + 1
                replace_list.append([start_index, end_index])
            except ValueError:
                if end_index < start_index:
                    raise InvalidInput("Unequal number of '\"'")
                break
        return replace_list

    @staticmethod
    def __switch_syntagms(expression, replace_list, escape_sequence):
        """ Method which goes through all syntagms in expression and switches them with new keys

            It dynamically creates new Keys for syntagms, then goes through list of syntagms (given by find_syntagm)
            and replaces each one with new key, and stores in escape_sequence (Key -> syntagm), which is necessary
            for later search. Syntagm is fixed in dictionary, (all special characters are removed, '"' are removed,
            and all additional spacing from beginning and end is removed)

            Keys all starts with PostfixParser.KEY_SIGN constant by which they are differed fom regular words
            (all keys are based $_KEY-X, where X is integer number, inspiration got from PHP notation)

            Args:
                expression - expression in which syntagms should be switched with new keys
                replace_list -  list of tuples with start and end indexes of all '"' signs
                        (should be retrieved from find_syntagm method)
                escape_sequence - (dict) which will be filled with new keys, which replaced syntagms

            Return:
                Expression with replaced all syntagms with special keys (stored into dictionary)
        """

        add_constant, key_constant = 0, 1
        key_escape = '_KEY-'
        for tuple_ in replace_list:
            current_escape = PostfixParser.KEY_SIGN + key_escape + str(key_constant)
            key_constant += 1
            escape_sequence[current_escape[1:]] = \
                expression[tuple_[0] + add_constant:tuple_[1] + add_constant + 1] \
                if tuple_[1] + add_constant + 1 < len(expression) else expression[tuple_[0] + add_constant:]

            expression = expression[:tuple_[0] + add_constant] + current_escape + \
                expression[tuple_[1] + add_constant + 1:] if tuple_[1] + add_constant + 1 < len(expression) \
                else expression[:tuple_[0] + add_constant] + current_escape

            add_constant = len(current_escape) - len(escape_sequence[current_escape[1:]])

            for key_word in PostfixParser.KEY_WORDS.keys():
                escape_sequence[current_escape[1:]] = escape_sequence[current_escape[1:]].replace(key_word, '')

            for key_word in PostfixParser.KEY_WORDS.values():
                if key_word != '':
                    escape_sequence[current_escape[1:]] = escape_sequence[current_escape[1:]].replace(key_word, '')

            escape_sequence[current_escape[1:]] = escape_sequence[current_escape[1:]][1:-1].strip()

        return expression

    @staticmethod
    def __insert_implied(token_list):
        """ Method which goes through token_list and inserts implied '&' sign before not signs if necessary

            It looks for expressions like "python NOT class" and adds implied AND so it gets "python AND NOT class"
            because NOT is looked as unary operator in every context.

            Because all work is done on list (and original is changed) nothing is returned.

            Args:
                token_list - list of tokens (words, operators and special keys) in which should be added AND signs
        """

        index_list = []
        for i, el in enumerate(token_list):
            if el == PostfixParser.KEY_WORDS['NOT']:
                if i == 0:
                    continue
                if token_list[i - 1] != '':
                    if token_list[i - 1] not in PostfixParser.OPERATORS.keys():
                        index_list.append(i)
                else:
                    if i - 2 >= 0 and token_list[i - 2] not in PostfixParser.OPERATORS.keys():
                        index_list.append(i)

        adding_const = 0
        for i in index_list:
            token_list.insert(i + adding_const, PostfixParser.KEY_WORDS['AND'])
            adding_const += 1

    @staticmethod
    def convert_postfix(expression, escape_sequences):
        """ Method which is called from outside, it does all the work and returns postfix list

            First it calls validate_expression method which does initial validation, then calls insert_implied method
            which insert implied signs, then checks for some errors which were not checked in validation
            (like "python AND AND object", or "AND object") if anything found it raises error.

            Those checks it does by looking at empty strings ('') inside token list (which are sign that two
            operators are next to each other).

            It uses Stack for internal postfix convert (and error checking like unequal number of parenthesis), and
            it populates escape_sequence dictionary with keys of syntagms if any found

            Args:
                expression - expression to be evaluated and converted
                escape_sequence - (dict) dictionary which should be filled with keys for syntagms if any found

            Return:
                List of tokens in postfix order, if validation is passed. And fills out dictionary with keys
                for syntagms if any is found

            Raise:
                InvalidInput - if any error while parsing is found
                (QuitRequest - if "QUIT" keyword was found)
        """

        token_list = PostfixParser.__validate_expression(expression, escape_sequences)
        PostfixParser.__insert_implied(token_list)
        postfix_list = []

        s = Stack()

        for index, element in enumerate(token_list):
            if element not in PostfixParser.OPERATORS and element != '':
                postfix_list.append(element)
                continue

            if element == '':
                try:
                    if index == 0:
                        if not PostfixParser.__check_right(token_list[index + 1]):
                            raise InvalidInput('Expression can not start with "%s"' % (token_list[index + 1]))
                    elif index == len(token_list) - 1:
                        if not PostfixParser.__check_left(token_list[index - 1]):
                            raise InvalidInput('Expression can not end with "%s"' % (token_list[index + 1]))
                    else:
                        # case: )(
                        if PostfixParser.__check_left(token_list[index - 1]) and PostfixParser.__check_right(token_list[index + 1])\
                                and token_list[index + 1] == '(':
                            raise InvalidInput('Wrong syntax. "%s %s"' % (token_list[index - 1], token_list[index + 1]))

                        # case ) NOT
                        if PostfixParser.__check_left(token_list[index - 1]) and PostfixParser.__check_right(token_list[index + 1])\
                                and token_list[index + 1] in PostfixParser.UNARY:
                            element = PostfixParser.KEY_WORDS['AND']
                            # must skip continue because of AND injection

                        # case: left doesn't match and right doesn't match
                        if not PostfixParser.__check_left(token_list[index - 1])\
                                and not PostfixParser.__check_right(token_list[index + 1]):
                            raise InvalidInput('Wrong syntax. "%s %s"' % (token_list[index - 1], token_list[index + 1]))

                        # case: ! ! (NOT NOT)
                        if PostfixParser.__check_right(token_list[index + 1]) and token_list[index + 1] in PostfixParser.UNARY \
                                and token_list[index - 1] in PostfixParser.UNARY:
                            raise InvalidInput("Wrong syntax. \"%s %s\"" % (token_list[index - 1], token_list[index + 1]))
                except IndexError:
                    raise InvalidInput("Wrong syntax")

            if element in PostfixParser.OPERATORS:
                if element == ')':
                    if s.is_empty():                    # case: ') ...'
                        raise InvalidInput('Unequal number of parenthesis')
                    while s.top() != '(':
                        postfix_list.append(s.pop())
                        if s.is_empty():                # case: unequal number of parenthesis
                            raise InvalidInput('Unequal number of parenthesis')
                    s.pop()     # poping '(' parenthesis
                    continue

                while not s.is_empty() and PostfixParser.OPERATORS[s.top()] >= PostfixParser.OPERATORS[element]:
                    if s.top() == '(':
                        break
                    postfix_list.append(s.pop())

                s.push(element)

        while not s.is_empty():
            if s.top() == '(':
                raise InvalidInput("Unequal number of parenthesis")
            postfix_list.append(s.pop())

        return postfix_list

    @staticmethod
    def calculate_postfix_list(postfix_list, whole_list, type_=LIST):
        """ Recursion based method which calculates postfix list by going through postfix list

            It goes through list and gets operators and operands which then passes to appropriate method
            and returns result (in base case it returns operand)

            Specification for this method is that it is designed to work with two kind of postfix list,
            one containing lists (lists of search results), and one containing integers (number of words in file),
            those two only differs in method-dictionary which is used for calculations.

            Use of this method needs some pre-work. It needs instead of words in original postfix list,
            list of results where those words occurs, or integers representing quantity of word in one file.

            NOTE: Shouldn't be passed original postfix list, because this method destroys list which gets, instead
            should be passed some copy of list.

            Args:
                postfix_list -  token list with postfix order, which should be calculated
                whole_list - side effect for logically unary operation (NOT) which essentially need two parameters
                type_ - (PostfixParser constant) flag which indicates which method-dictionary should be used
        """

        # base case for recursion
        if isinstance(postfix_list[-1], list) or isinstance(postfix_list[-1], int):
            list_ = postfix_list[-1]
            del postfix_list[-1]
            return list_

        # binary operators
        if postfix_list[-1] in PostfixParser.OPERATORS and postfix_list[-1] not in PostfixParser.UNARY:
            operator = postfix_list[-1]
            del postfix_list[-1]

            second = PostfixParser.calculate_postfix_list(postfix_list, whole_list, type_)
            first = PostfixParser.calculate_postfix_list(postfix_list, whole_list, type_)

            return PostfixParser.LIST_METHODS[operator](first, second) if type_ == PostfixParser.LIST\
                else PostfixParser.INT_METHODS[operator](first, second)

        # logically unary, physically binary..
        if postfix_list[-1] in PostfixParser.UNARY:
            operator = postfix_list[-1]
            del postfix_list[-1]

            number = PostfixParser.calculate_postfix_list(postfix_list, whole_list, type_)

            return PostfixParser.LIST_METHODS[operator](number, whole_list) if type_ == PostfixParser.LIST \
                else PostfixParser.INT_METHODS[operator](number, whole_list)

    @staticmethod
    def __check_right(element):
        """ Side method for checking the right side

            Method checks if element passed to it can be at right side of some other operator

            Args:
                element - (string - operator) which should be checked if can be on right side of other operator

            Return:
                True if can, False if cannot
        """

        if element in '(' or element in PostfixParser.UNARY:
            return True
        return False

    @staticmethod
    def __check_left(element):
        """ Side method for checking the left side

            Method checks if element passed to it can be at left side of some other operator

            Args:
                element - (string - operator) which should be checked if can be on left side of other operator

            Return:
                True if can, False if cannot
        """

        if element in ')':
            return True
        return False