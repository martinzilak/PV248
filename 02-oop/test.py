#!/usr/bin/env python

from sys import argv
from enum import Enum
from scorelib import Print, Edition, Composition, Voice, Person, Line
import re

editions = []

regex = {
    'NUMBER': re.compile(r'\d+'),
    'ANYTHING_AFTER_COLON': re.compile(r':(.*)'),
    'COMPOSER_YEARS': re.compile(r'(.+?)\((\d*)(?:\/\d)?(-{1,2}|\+|\*)(\d*).*\)'),
    'Y': re.compile(r'y'),
    'COMPOSITION_YEAR': re.compile(r'\d{3,}')
}

def parseComposer(line):
    authors = []
    for composer in line.split(';'):
        composer = composer.strip()
        person = Person()
        if regex['COMPOSER_YEARS'].match(composer):
            match = regex['COMPOSER_YEARS'].match(composer)
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

def starts(line, linetype):
    return line.lower().startswith(linetype.value.lower())

def parse(_temp, line):
    if starts(line, Line.PRINT_NUMBER):
        _temp['print'].print_id = regex['NUMBER'].match(line)
    elif starts(line, Line.COMPOSER):
        _temp['composition'].authors = parseComposer(regex['ANYTHING_AFTER_COLON'].match(line).group(1))
    elif starts(line, Line.TITLE):
        _temp['composition'].name = regex['ANYTHING_AFTER_COLON'].match(line).group(1).strip()
    elif starts(line, Line.GENRE):
        _temp['composition'].genre = regex['ANYTHING_AFTER_COLON'].match(line).group(1).strip()
    elif starts(line, Line.KEY):
        _temp['composition'].key = regex['ANYTHING_AFTER_COLON'].match(line).group(1).strip()
    elif starts(line, Line.COMPOSITION_YEAR):
        _temp['composition'].year = regex['COMPOSITION_YEAR'].match(line)
    elif starts(line, Line.PUBLICATION_YEAR):
        pass
    elif starts(line, Line.EDITION):
        _temp['edition'] = parseEdition(regex['ANYTHING_AFTER_COLON'].match(line).group(1).strip())
    elif starts(line, Line.EDITOR):
        pass
    elif starts(line, Line.VOICE):
        pass
    elif starts(line, Line.PARTITURE):
        _temp['print'].partiture = True if regex['Y'].match(line) else False
    elif starts(line, Line.INCIPIT):
        _temp['composition'].incipit = regex['ANYTHING_AFTER_COLON'].match(line).group(1).strip()

def process(block):
    _print = Print()
    composition = Composition()
    edition = Edition()
    _temp = {'print': _print, 'composition': composition, 'edition': edition}

    for line in block:
        parse(_temp, line)

    edition.composition = composition
    _print.edition = edition

    return _print

def load(filename):
    prints = []
    blocks = []
    reading = []

    with open(filename, errors='ignore') as file:
        for line in file:
            if line != '\n':
                reading.append(line)
            else:
                blocks.append(reading)
                reading = []

    for block in blocks:
        prints.append(process(block))

    return sorted(prints, key = lambda x: x.print_id)

def main():
    if len(argv) != 2:
        raise ValueError('Wrong number of arguments passed')

    for _print in load(argv[1]):
        _print.format()
        print('\n')

if __name__ == '__main__':
    main()
