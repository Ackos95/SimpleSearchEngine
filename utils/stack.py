__author__ = 'Acko'


class StackEmptyError(Exception):
    """ Error raised if stack is empty, and pop or top methods are called """
    pass


class Stack:
    """ Classic stack """

    __slots__ = ['data']

    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def push(self, el):
        self.data.append(el)

    def pop(self):
        if len(self.data) == 0:
            raise StackEmptyError('Stack is empty')

        return self.data.pop()

    def top(self):
        if len(self.data) == 0:
            raise StackEmptyError('Stack is empty')

        return self.data[-1]

    def is_empty(self):
        return len(self.data) == 0