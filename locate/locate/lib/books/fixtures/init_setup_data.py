from lino.utils.instantiator import Instantiator

from locate.lib.books.fixtures.setup_data import *

from collections import namedtuple

INSTANTIATOR_ITER = namedtuple('INSTANTIATOR_ITER', 'instantiator data')


Category = Instantiator('books.Category', 'name').build
Author = Instantiator('books.Author', 'name').build
Publication = Instantiator('books.Publication', 'name').build
BookInfo = Instantiator('books.BookInfo', 'name author:name publication:name category:name copies').build
Book = Instantiator('books.Book', 'code info:name').build


def read_data(data):
    '''
    Reads data line by line.

    :param data:
    :return: a list of data
    '''
    return (d.split('^') for d in data.splitlines()[1:])    # remove 1st empty line.


def objects():
    # Setup tables
    instantiators = [INSTANTIATOR_ITER(Category, CATEGORY_DATA), INSTANTIATOR_ITER(Author, AUTHOR_DATA),
                        INSTANTIATOR_ITER(Publication, PUBLICATION_DATA), INSTANTIATOR_ITER(BookInfo, BOOK_INFO_DATA),
                        INSTANTIATOR_ITER(Book, BOOK_DATA)]
    for i in instantiators:
        for row in read_data(i.data):
            yield i.instantiator(*row)
