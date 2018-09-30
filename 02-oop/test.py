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
    'COMPOSITION_YEAR': r'.*?(\d{3,})',
    'VOICE': r'\s*(?:(\S+?)(-{1,2})(\S+?)(?:,|;)\s*){0,1}(.*)',
    'EDITOR': r'(?:(?:[^\,]+\.?)(?:\,?\s+))?(?:[^\,]+\.?)'
}

def parseSimple(line, regex, group = 1, defval = None, parseint = False):
    r = re.compile(Regex[regex])
    m = r.match(line)
    if m:
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
        return ''
    return name

def parseEditor(line):
    editors = []
    if line == None:
        return editors
    r = re.compile(Regex['EDITOR'])
    m = r.findall(line)
    for name in m:
        p = Person()
        p.name = name.strip()
        editors.append(p)
    return editors

def parseVoice(line):
    v = Voice()
    if line == None:
        return v
    r = re.compile(Regex['VOICE'])
    m = r.match(line.strip())
    if m:
        v.name = m.group(4)
        range = ''
        if m.group(1):
            range += m.group(1)
        range += '--'
        if m.group(3):
            range += m.group(3)
        v.range = range if len(range) > 2 else None
    return v

def parsePartiture(line):
    return True if parseSimple(line, 'Y') else False

def starts(line, linetype):
    return line.lower().startswith(linetype.value.lower())

def parse(_temp, line):
    if starts(line, Line.PRINT_NUMBER):
        _temp['print'].print_id = parseSimple(line, 'NUMBER', parseint = True)
    elif starts(line, Line.COMPOSER):
        _temp['composition'].authors = parseComposer(parseSimple(line, 'ANYTHING_AFTER_COLON'))
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
        _temp['edition'].name = parseSimple(line, 'ANYTHING_AFTER_COLON')
    elif starts(line, Line.EDITOR):
        _temp['edition'].authors = parseEditor(parseSimple(line, 'ANYTHING_AFTER_COLON'))
    elif starts(line, Line.VOICE):
        _temp['voices'].append(parseVoice(parseSimple(line, 'ANYTHING_AFTER_COLON')))
    elif starts(line, Line.PARTITURE):
        _temp['print'].partiture = parsePartiture(line)
    elif starts(line, Line.INCIPIT):
        _temp['composition'].incipit = parseSimple(line, 'ANYTHING_AFTER_COLON')

def process(block):
    _print = Print()
    composition = Composition()
    edition = Edition()
    voices = []
    _temp = {'print': _print, 'composition': composition, 'edition': edition, 'voices': voices}

    for line in block:
        parse(_temp, line)

    composition.voices = voices
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
        blocks.append(reading)

    for block in blocks:
        prints.append(process(block))

    return list(filter(lambda y: y.print_id >= 0, sorted(prints, key = lambda x: x.print_id)))

def main():
    if len(argv) != 2:
        raise ValueError('Wrong number of arguments passed')

    for _print in load(argv[1]):
        _print.format()

if __name__ == '__main__':
    main()
