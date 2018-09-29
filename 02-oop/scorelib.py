from enum import Enum

class Print:
    def __init__(self, edition = None, print_id = -1, partiture = False):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture

    def format(self):
        if(self.print_id):
            print(Line.PRINT_NUMBER.value, ': ', self.print_id, sep = '', end = '\n')
        if(len(self.composition().authors) > 0):
            print(Line.COMPOSER.value, ': ', sep='', end=' ')
            for c in self.composition().authors:
                print(c.name, sep='', end=' ')
                if c.born or c.died:
                    print('(', sep='', end='')
                    if c.born:
                        print(c.born, sep='', end='')
                    print('--', sep='', end='')
                    if c.died:
                        print(c.died, sep='', end='')
                    print(')', sep='', end='')
                if c == self.composition().authors[-1]:
                    print('\n', sep='', end='')
                else:
                    print('; ', sep='', end='')
        if (self.composition().name):
            print(Line.TITLE.value, ': ', self.composition().name, sep='', end='\n')
        if ():
            print(Line.GENRE.value, ': ', self.composition().genre, sep='', end='\n')
        if (self.composition().genre):
            print(Line.KEY.value, ': ', self.composition().key, sep='', end='\n')
        if (self.composition().year):
            print(Line.COMPOSITION_YEAR.value, ': ', self.composition().year, sep='', end='\n')
        if (self.edition.name):
            print(Line.EDITION.value, ': ', self.edition.name, sep='', end='\n')
        if (len(self.edition.authors) > 0):
            print(Line.EDITOR.value, ': ', sep='', end='')
            for e in self.edition.authors:
                print(e.name, sep='', end=' ')
                if e == self.edition.authors[-1]:
                    print('\n', sep='', end='')
                else:
                    print('; ', sep='', end='')
        if (len(self.composition().voices) > 0):
            for v in self.composition().voices:
                print(Line.VOICE.value, ' ', self.composition().voices.index(v), ': ',  sep='', end='')
                if v.range:
                    print(v.range, sep='', end=', ')
                if v.name:
                    print(v.name, sep='', end='')
                print('\n', sep='', end='')
        print(Line.PARTITURE.value, ': ', 'yes' if self.partiture else 'no', sep='', end='\n')
        if (self.composition().incipit):
            print(Line.INCIPIT.value, ': ', self.composition().incipit, sep='', end='\n')

    def composition(self):
        return self.edition.composition

class Edition:

    editions = []

    def __init__(self, composition = None, authors = [], name = None):
        self.composition = composition
        self.authors = authors
        self.name = name

    @classmethod
    def get(cls, name):
        for x in cls.editions:
            if x.name == name:
                return x
        e = Edition(name = name)
        cls.editions.append(e)
        return e

class Composition:
    def __init__(self, name = None, incipit = None, key = None, genre = None, year = None, voices = [], authors = []):
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

class Line(Enum):
    PRINT_NUMBER = 'Print Number'
    COMPOSER = 'Composer'
    TITLE = 'Title'
    GENRE = 'Genre'
    KEY = 'Key'
    COMPOSITION_YEAR = 'Composition Year'
    PUBLICATION_YEAR = 'Publication Year'
    EDITION = 'Edition'
    EDITOR = 'Editor'
    VOICE = 'Voice'
    PARTITURE = 'Partiture'
    INCIPIT = 'Incipit'