from enum import Enum

class Composition:
    def __init__(self, name = None, incipit = None, key = None, genre = None, year = None, voices = [], authors = []):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voices = voices
        self.authors = authors

    def format1(self):
        if(len(self.authors) > 0 and len(self.formatAuthors()) > 0):
            print('{}: {}'.format(Line.COMPOSER.value, self.formatAuthors()))
        if(self.name):
            print('{}: {}'.format(Line.TITLE.value, self.name))
        if(self.genre):
            print('{}: {}'.format(Line.GENRE.value, self.genre))
        if(self.key):
            print('{}: {}'.format(Line.KEY.value, self.key))
        if(self.year):
            print('{}: {}'.format(Line.COMPOSITION_YEAR.value, self.year))

    def format2(self):
        if(len(self.voices) > 0):
            i = 0
            for v in self.voices:
                if(v.name or v.range):
                    i += 1
                    print('{} {}: {}'.format(Line.VOICE.value, i, v.formatted()))

    def formatAuthors(self):
        formatted = ''
        for a in self.authors:
            formatted += a.formatted() + "; "
        return formatted[:-2]

class Edition:
    def __init__(self, composition = Composition(), authors = [], name = None):
        self.composition = composition
        self.authors = authors
        self.name = name

    def format(self):
        self.composition.format1()
        if(self.name):
            print('{}: {}'.format(Line.EDITION.value, self.name))
        if(len(self.authors) > 0):
            print('{}: {}'.format(Line.EDITOR.value, self.formatAuthors()))
        self.composition.format2()

    def formatAuthors(self):
        formatted = ''
        for a in self.authors:
            formatted += a.formatted() + ", "
        return formatted[:-2]

class Print:
    def __init__(self, edition = Edition(), print_id = -1, partiture = False):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture

    def format(self):
        print('{}: {}'.format(Line.PRINT_NUMBER.value, self.print_id))
        self.edition.format()
        print('{}: {}'.format(Line.PARTITURE.value, 'yes' if self.partiture else 'no'))
        if(self.composition().incipit):
            print('{}: {}'.format(Line.INCIPIT.value, self.composition().incipit))
        print()

    def composition(self):
        return self.edition.composition

class Voice:
    def __init__(self, name = None, range = None):
        self.name = name
        self.range = range

    def formatted(self):
        return ('{}, '.format(self.range) if self.range else '') + (self.name if self.name else '')

class Person:
    def __init__(self, name = None, born = None, died = None):
        self.name = name
        self.born = born
        self.died = died

    def formatted(self):
        formatted = self.name
        if self.born or self.died:
            formatted += '({}--{})'.format(self.born if self.born else '', self.died if self.died else '')
        return formatted

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