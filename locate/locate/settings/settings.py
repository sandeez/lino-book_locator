from lino.projects.std.settings import *

class Site(Site):
    title = 'Book Locator'
    demo_fixtures = ['init_setup_data']

    def setup_menu(self, profile, main):
        # set Admin menu
        m = main.add_menu('administrator', 'Administrator')

        # set accommodation
        sm1 = m.add_menu('accommodation', 'Accommodation')
        sm1.add_action(self.modules.books.Floors)
        sm1.add_action(self.modules.books.Rooms)
        sm1.add_action(self.modules.books.Bookshelves)
        sm1.add_action(self.modules.books.Racks)
        sm1.add_action(self.modules.books.Slots)

        # set books and their information
        sm2 = m.add_menu('books_details', 'Books Details')
        sm2.add_action(self.modules.books.Categories)
        sm2.add_action(self.modules.books.Publications)
        sm2.add_action(self.modules.books.Authors)
        sm2.add_action(self.modules.books.BookInformation)
        sm2.add_action(self.modules.books.Books)
        sm2.add_action(self.modules.books.BookLocations)

    def get_admin_main_items(self, ar):
        yield self.modules.books.BooksToBeTagged
        yield self.modules.books.BooksToBeArranged
        yield self.modules.books.AvailableSlots

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'locate.lib.books'


SITE = Site(globals())
DEBUG = True
