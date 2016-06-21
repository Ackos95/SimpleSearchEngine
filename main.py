"""
    Starting point of program...
"""

__author__ = 'Acko'

import os

from search.search import Search
from utils.postfix_parser import InvalidInput, QuitRequest


if __name__ == '__main__':
    initial_path = raw_input("Unesite putanju do baze: ")
    Search.print_instruction()
    print 'Ucitavanje. Molim vas sacekajte...'
    s = Search(os.path.abspath(initial_path))

    while True:
        try:
            s.find_expression(raw_input("Unesite reci za pretragu (ili 'QUIT' za izlaz): "))
        except InvalidInput:
            print "Pogresno unet zahtev, pokusajte ponovo."
        except QuitRequest:
            break

    print 'Dovidjenja'