#!/usr/bin/env python

from sys import argv
from enum import Enum
from os import linesep
from .scorelib import Print, Edition, Composition, Voice, Person
import re

editions = []

class Regex(Enum):
    NUM = re.compile(r'\d+')

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
    EMPTY = ''

def starts(line, linetype):
    return line.lower().startswith(linetype.lower())

def parse(_print, line):
    if starts(line, Line.PRINT_NUMBER):
        _print.print_id = Regex.NUM.match(line)
    elif starts(line, Line.COMPOSER):
        pass
    elif starts(line, Line.TITLE):
        pass
    elif starts(line, Line.GENRE):
        pass
    elif starts(line, Line.KEY):
        pass
    elif starts(line, Line.COMPOSITION_YEAR):
        pass
    elif starts(line, Line.PUBLICATION_YEAR):
        pass
    elif starts(line, Line.EDITION):
        pass
    elif starts(line, Line.EDITOR):
        pass
    elif starts(line, Line.VOICE):
        pass
    elif starts(line, Line.PARTITURE):
        pass
    elif starts(line, Line.INCIPIT):
        pass

def process(block):
    _print = Print()

    for line in block.split(linesep):
        parse(_print, line)

    return _print

def load(filename):
    prints = []

    with open(filename, errors='ignore') as file:
        for block in file.read().split(linesep+linesep):
            prints.append(process(block))

    return sorted(prints, key = lambda x: x.print_id)

def main():
    if len(argv) != 2:
        raise ValueError('Wrong number of arguments passed')

    for _print in load(argv[1]):
        _print.format()
        print(linesep)

if __name__ == '__main__':
    main()