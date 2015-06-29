from django.db.models import Count, Q

from lino.api import dd

from .models import BookInfo


class Floors(dd.Table):
    model = 'Floor'
    column_names = 'number'


class Rooms(dd.Table):
    model = 'Room'
    column_names = 'number name floor'



class Bookshelves(dd.Table):
    model = 'Bookshelf'
    column_names = 'code room room__floor'


class Racks(dd.Table):
    model = 'Rack'
    column_names = 'code bookshelf bookshelf__room bookshelf__room__floor'


class Slots(dd.Table):
    model = 'Slot'
    column_names = 'number rack rack__bookshelf rack__bookshelf__room rack__bookshelf__room__floor'


class Categories(dd.Table):
    model = 'Category'
    order_by = ['name']
    column_names = 'name'


class Authors(dd.Table):
    model = 'Author'
    column_names = 'name'
    order_by = ['name']
    insert_layout = '''
    name
    '''


class Publications(dd.Table):
    model = 'Publication'
    column_names = 'name'
    order_by = ['name']


class BookInformation(dd.Table):
    model = 'BookInfo'
    column_names = 'name author publication category copies'
    order_by = ['name', 'author', 'publication', 'category']
    detail_layout = '''
    name author publication category copies
    BooksInfoByAuthor
    '''


class BooksInfoByAuthor(BookInformation):
    master_key = 'author'


class Books(dd.Table):
    model = 'Book'
    column_names = 'code info info__author info__publication info__category'
    order_by = ['code', 'info', 'info__author', 'info__publication', 'info__category']


class BooksLocation(dd.Table):
    model = 'BookLocation'
    column_names = 'book slot'
    order_by = ['book']
    detail_layout = '''
    book slot
    BooksLocationByBook BooksLocationBySlot
    '''


class BooksLocationByBook(BooksLocation):
    master_key = 'book'
    column_names = 'book book__info'


class BooksLocationBySlot(BooksLocation):
    master_key = 'slot'
    column_names = 'slot slot__rack'


class AvailableSlots(Slots):
    label = 'Available Slots'
    column_names = 'number rack'
    order_by = ['number', 'rack']

    @classmethod
    def get_request_queryset(cls, ar):
        qs_slot = super(AvailableSlots, cls).get_request_queryset(ar)
        return qs_slot.exclude(booklocation__in=qs_slot)


class BooksToBeTagged(dd.VirtualTable):
    label = "Books to be Tagged"
    column_names = 'count copies name'

    @classmethod
    def get_data_rows(cls, ar):
        qs_book_info = BookInfo.objects.values('name', 'copies').annotate(count=Count('book'))
        qs_book_to_be_tagged = []
        for item in qs_book_info:
            if item['count'] < item['copies']:
                item['count'] = item['copies'] - item['count']
                qs_book_to_be_tagged.append(item)
        return qs_book_to_be_tagged

    @dd.displayfield('Name')
    def name(cls, row, ar):
        return row['name']

    @dd.displayfield('Total No. of Book Copies')
    def copies(cls, row, ar):
        return str(row['copies'])

    @dd.displayfield('Total No. of Books to be Tagged')
    def count(cls, row, ar):
        return str(row['count'])


class BooksToBeArranged(Books):
    label = "Books to be Arranged"
    column_names = 'code info'
    order_by = ['code', 'info']

    @classmethod
    def get_request_queryset(cls, ar):
        qs_books_info = super(BooksToBeArranged, cls).get_request_queryset(ar)
        return qs_books_info.exclude(booklocation=qs_books_info)