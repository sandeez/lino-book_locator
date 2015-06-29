from lino.utils.instantiator import Instantiator

from locate.lib.books.fixtures.setup_data import *


Category = Instantiator('books.Category', 'name').build
Author = Instantiator('books.Author', 'name').build
Publication = Instantiator('books.Publication', 'name').build
BookInfo = Instantiator('books.BookInfo', 'name author publication category copies').build


def read_data(data):
    '''
    Reads data line by line.

    :param data:
    :return: a list of data
    '''
    return (d.split('^') for d in data.splitlines()[1:])    # remove 1st empty line.


def objects():
    # Setup tables
    instantiators = {Category: CATEGORY_DATA, Author: AUTHOR_DATA, Publication: PUBLICATION_DATA,
                     # BookInfo: BOOK_INFO_DATA
                     }
    for i, d in instantiators.iteritems():
        for row in read_data(d):
            yield i(*row)
    # yield BookInfo('Mrutyunjay', '4', '5', '15', '10')

if __name__ == '__main__':
    objects()