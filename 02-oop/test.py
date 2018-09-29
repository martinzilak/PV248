#!/usr/bin/env python

from sys import argv
from enum import Enum
from scorelib import Print, Edition, Composition, Voice, Person, Line
import re

Regex = {
    'NUMBER': r'.*?(\d+)',
    'ANYTHING_AFTER_COLON': r'.*?:(.*)',
    'COMPOSER': r'(.+?)\((\d*)(-{1,2}|\+|\*)(\d*)\)',
    'Y': r'.*?(y)',
    'COMPOSITION_YEAR': r'.*?(\d{3,})'
}

def parseSimple(line, regex, group = 1, defval = None, parseint = False):
    r = re.compile(Regex[regex])
    m = r.match(line)
    print(line, 're:', Regex[regex], r, '\nmatch:', m, '\n')
    if m:
        if group != 0:
            m = m.group(group)
        return m.strip() if not parseint else int(m.strip())
    return defval

def parseComposer(line):
    if line == None:
        return []
    authors = []
    for composer in line.split(';'):
        composer = composer.strip()
        person = Person()
        r = re.compile(Regex['COMPOSER'])
        m = r.match(composer)
        if m:
            person.name = m.group(1)
            if m.group(2):
                person.born = int(m.group(2))
            if m.group(4):
                if m.group(3) == '*':
                    person.born = m.group(4)
                else:
                    person.died = m.group(4)
        else:
            person.name = composer
        authors.append(person)
    return authors

def parseEdition(name):
    if name == None:
        return None
    return Edition.get(name = name)

def parsePartiture(line):
    return True if parseSimple(line, 'Y') else False

def starts(line, linetype):
    return line.lower().startswith(linetype.value.lower())

def parse(_temp, line):
    if starts(line, Line.PRINT_NUMBER):
        _temp['print'].print_id = parseSimple(line, 'NUMBER', parseint = True)
    elif starts(line, Line.COMPOSER):
        _temp['composition'].authors = parseSimple(line, 'ANYTHING_AFTER_COLON')
    elif starts(line, Line.TITLE):
        _temp['composition'].name = parseSimple(line, 'ANYTHING_AFTER_COLON')
    elif starts(line, Line.GENRE):
        _temp['composition'].genre = parseSimple(line, 'ANYTHING_AFTER_COLON')
    elif starts(line, Line.KEY):
        _temp['composition'].key = parseSimple(line, 'ANYTHING_AFTER_COLON')
    elif starts(line, Line.COMPOSITION_YEAR):
        _temp['composition'].year = parseSimple(line, 'COMPOSITION_YEAR', parseint = True)
    elif starts(line, Line.PUBLICATION_YEAR):
        pass
    elif starts(line, Line.EDITION):
        _temp['edition'] = parseEdition(parseSimple(line, 'ANYTHING_AFTER_COLON'))
    elif starts(line, Line.EDITOR):
        pass
    elif starts(line, Line.VOICE):
        pass
    elif starts(line, Line.PARTITURE):
        _temp['print'].partiture = parsePartiture(line)
    elif starts(line, Line.INCIPIT):
        _temp['composition'].incipit = parseSimple(line, 'ANYTHING_AFTER_COLON')

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
