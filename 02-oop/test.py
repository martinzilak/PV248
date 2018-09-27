#!/usr/bin/env python

from sys import argv
from enum import Enum
from os import linesep
from scorelib import Print, Edition, Composition, Voice, Person, Line
import re

editions = []

class Regex(Enum):
    NUMBER = re.compile(r'\d+')
    ANYTHING_AFTER_COLON = re.compile(r':(.*)')
    COMPOSER_YEARS = re.compile(r'(.+?)\((\d*)(?:\/\d)?(-{1,2}|\+|\*)(\d*).*\)')
    Y = re.compile(r'y')
    COMPOSITION_YEAR = re.compile(r'\d{3,}')

def starts(line, linetype):
    return line.lower().startswith(linetype.value.lower())

def parse(_temp, line):
    if starts(line, Line.PRINT_NUMBER):
        _temp['print'].print_id = Regex.NUMBER.value.match(line)
    elif starts(line, Line.COMPOSER):
        _temp['composition'].authors = parseComposer(Regex.ANYTHING_AFTER_COLON.value.match(line).group(1))
    elif starts(line, Line.TITLE):
        _temp['composition'].name = Regex.ANYTHING_AFTER_COLON.value.match(line).group(1).strip()
    elif starts(line, Line.GENRE):
        _temp['composition'].genre = Regex.ANYTHING_AFTER_COLON.value.match(line).group(1).strip()
    elif starts(line, Line.KEY):
        _temp['composition'].key = Regex.ANYTHING_AFTER_COLON.value.match(line).group(1).strip()
    elif starts(line, Line.COMPOSITION_YEAR):
        _temp['composition'].year = Regex.COMPOSITION_YEAR.value.match(line)
    elif starts(line, Line.PUBLICATION_YEAR):
        pass
    elif starts(line, Line.EDITION):
        _temp['edition'] = parseEdition(Regex.ANYTHING_AFTER_COLON.value.match(line).group(1).strip())
    elif starts(line, Line.EDITOR):
        pass
    elif starts(line, Line.VOICE):
        pass
    elif starts(line, Line.PARTITURE):
        _temp['print'].partiture = True if Regex.Y.value.match(line) else False
    elif starts(line, Line.INCIPIT):
        _temp['composition'].incipit = Regex.ANYTHING_AFTER_COLON.value.match(line).group(1).strip()

def process(block):
    _print = Print()
    composition = Composition()
    edition = Edition()
    _temp = {'print': _print, 'composition': composition, 'edition': edition}

    for line in block.split(linesep):
        parse(_temp, line)

    edition.composition = composition
    _print.edition = edition

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

def parseComposer(line):
    authors = []
    for composer in line.split(';'):
        composer = composer.strip()
        person = Person()
        if Regex.COMPOSER_YEARS.match(composer):
            match = Regex.COMPOSER_YEARS.match(composer)
            person.name = match.group(1)
            if match.group(2):
                person.born = int(match.group(2))
            if match.group(4):
                if match.group(3) == '*':
                    person.born = match.group(4)
                else:
                    person.died = match.group(4)
        else:
            person.name = composer
        authors.append(person)
    return authors

def parseEdition(name):
    return Edition.get(name = name)