from lino.utils.instantiator import Instantiator
from lino.utils.cycler import Cycler

from locate.lib.books.fixtures.setup_data import *



def read_data(data):
    '''
    Reads data line by line.

    :param data:
    :return: a list of data
    '''
    return (d.split('^') for d in data.splitlines()[1:])    # remove 1st empty line.


def objects():
    Category = Instantiator('books.Category', 'name').build
    Author = Instantiator('books.Author', 'name').build
    Publication = Instantiator('books.Publication', 'name').build
    BookInfo = Instantiator('books.BookInfo', 'name author:name publication category copies').build

    # Setup tables
    instantiators = (
        (Category, CATEGORY_DATA),
        (Author, AUTHOR_DATA),
        (Publication, PUBLICATION_DATA),
        (BookInfo, BOOK_INFO_DATA))
    for i, d in instantiators:
        print i
        for row in read_data(d):
            # print row
            yield i(*row)
    # yield BookInfo('Mrutyunjay', '4', '5', '15', '10')

    # added by LS:
    from lino.api import rt
    Floor = rt.modules.books.Floor
    Room = rt.modules.books.Room
    Bookshelf = rt.modules.books.Bookshelf
    Rack = rt.modules.books.Rack
    Slot = rt.modules.books.Slot
    Book = rt.modules.books.Book
    BookInfo = rt.modules.books.BookInfo
    BookLocation = rt.modules.books.BookLocation
    for i in range(10):
        floor = Floor(number=i)
        yield floor
        for j, name in enumerate(["first", "second", "third"]):
            room = Room(floor=floor, number=j, name=name)
            yield room
            for code in ("A", "B", "C"):
                shelf = Bookshelf(room=room, code=code)
                yield shelf
                for rack_code in ("D", "E", "F"):
                    rack = Rack(bookshelf=shelf, code=rack_code)
                    yield rack

                    for slot_number in (1, 2, 3, 4):
                        slot = Slot(rack=rack, number=slot_number)
                        yield slot

    unique_code = 1
    # create 2 copies (Book) of each BookInfo:
    for info in BookInfo.objects.all():
        for i in range(2):
            yield Book(info=info, code=str(unique_code))
            unique_code += 1
    SLOTS = Cycler(Slot.objects.all())
    for book in Book.objects.all():
        yield BookLocation(book=book, slot=SLOTS.pop())
    

if __name__ == '__main__':
    objects()
