from lino.api import dd
from django.db import models


class Floor(dd.Model):
    number = models.IntegerField('Number', null=False)

    def __unicode__(self):
        return 'Floor: {0}'.format(self.number)

    class Meta:
        verbose_name = 'Floor'
        verbose_name_plural = 'Floors'


class Room(dd.Model):
    number = models.IntegerField('Number', null=False)
    name = models.CharField('Name', max_length=10)
    floor = models.ForeignKey(Floor)

    def __unicode__(self):
        return 'Floor: {0} -> Room: {1}'.format(
                    self.floor.number,
                    self.number)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        unique_together = ('number', 'floor')


class Bookshelf(dd.Model):
    code = models.CharField('Code', null=False, max_length=5)
    room = models.ForeignKey(Room)

    def __unicode__(self):
        return 'Floor: {0} -> Room: {1} -> Bookshelf: {2}'.format(
                    self.room.floor.number,
                    self.room.number,
                    self.code)

    class Meta:
        verbose_name = 'Bookshelf'
        verbose_name_plural = 'Bookshelves'
        unique_together = ('code', 'room')


class Rack(dd.Model):
    code = models.CharField('Code', max_length=5, null=False)
    bookshelf = models.ForeignKey(Bookshelf)

    def __unicode__(self):
        return 'Floor: {0} -> Room: {1} -> Bookshelf: {2} -> Rack: {3}'.format(
                    self.bookshelf.room.floor.number,
                    self.bookshelf.room.number,
                    self.bookshelf.code,
                    self.code)

    class Meta:
        verbose_name = 'Rack'
        verbose_name_plural = 'Racks'
        unique_together = ('code', 'bookshelf')


class Slot(dd.Model):
    number = models.IntegerField('Number', null=False)
    rack = models.ForeignKey(Rack)

    def __unicode__(self):
        return 'Floor: {0} -> Room: {1} -> Bookshelf: {2} -> Rack: {3} -> Slot: {4}'.format(
                    self.rack.bookshelf.room.floor.number,
                    self.rack.bookshelf.room.number,
                    self.rack.bookshelf.code,
                    self.rack.code,
                    self.number)

    class Meta:
        verbose_name = 'Slot'
        verbose_name_plural = 'Slots'
        unique_together = ('number', 'rack')


class Category(dd.Model):
    name = models.CharField(null=False, max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Author(dd.Model):
    name = models.CharField(null=False, max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Publication(dd.Model):
    name = models.CharField(null=False, max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'


class BookInfo(dd.Model):
    name = models.CharField('Name', max_length=50)
    author = models.ForeignKey(Author)
    publication = models.ForeignKey(Publication)
    category = models.ForeignKey(Category)
    copies = models.IntegerField('Total Copies', null=False, default=1)

    def __unicode__(self):
        return 'Name: {0} -> Author: {1} -> Publication: {2}'.format(
                    self.name,
                    self.author,
                    self.publication)

    class Meta:
        verbose_name = 'Book Information'
        verbose_name_plural = 'Books Information'
        unique_together = ('name', 'author', 'publication')


class Book(dd.Model):
    code = models.CharField(max_length=10, unique=True)
    info = models.ForeignKey(BookInfo)

    def __unicode__(self):
        return 'Code: {0} -> Name: {1} -> Author: {2}'.format(
                    self.code,
                    self.info.name,
                    self.info.author)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        unique_together = ('code', 'info')


class BookLocation(dd.Model):
    book = models.ForeignKey(Book, unique=True)
    slot = models.ForeignKey(Slot, unique=True)

    def __unicode__(self):
        return 'Floor: {0} -> Room: {1} -> Bookshelf: {2} -> Rack:{3} -> Slot: {4} -> Book: {5}'.format(
                    self.slot.rack.bookshelf.room.floor.number,
                    self.slot.rack.bookshelf.room.number,
                    self.slot.rack.bookshelf.code,
                    self.slot.rack.code,
                    self.slot.number,
                    self.book.code)

    class Meta:
        verbose_name = 'Book Location'
        verbose_name_plural = 'Book Locations'


from .ui import *
