from enum import Enum

class Print:
    def __init__(self, edition = None, print_id = None, partiture = None):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture

    def format(self):
        print(Line.PRINT_NUMBER.value, ': ', self.print_id, sep = '', end = '\n')

    def composition(self):
        return self.edition.composition

class Edition:

    editions = []

    def __init__(self, composition = None, authors = [], name = None):
        self.composition = composition
        self.authors = authors
        self.name = name

    def get(self, name):
        return next((x for x in self.editions if x.name == name), Edition(name = name))

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