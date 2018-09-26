class Print:
    def __init__(self, edition = None, print_id = None, partiture = None):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture

    '''
    @property
    def edition(self):
        return self._edition

    @edition.setter
    def edition(self, edition):
        self._edition = edition

    @property
    def print_id(self):
        return self._print_id

    @print_id.setter
    def print_id(self, print_id):
        self._print_id = print_id

    @property
    def partiture(self):
        return self._partiture

    @partiture.setter
    def partiture(self, partiture):
        self._partiture = partiture
    '''

    def format(self):
        pass

    def composition(self):
        return self.edition.composition

class Edition:
    def __init__(self, composition = None, authors = None, name = None):
        self.composition = composition
        self.authors = authors
        self.name = name

class Composition:
    def __init__(self, name = None, incipit = None, key = None, genre = None, year = None, voices = None, authors = None):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voices = voices
        self.authors = authors

class Voice:
    def __init__(self, name = None, range = None):
        self.name = name
        self.range = range

class Person:
    def __init__(self, name = None, born = None, died = None):
        self.name = name
        self.born = born
        self.died = died