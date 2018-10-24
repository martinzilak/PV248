#!/usr/bin/env python

from sys import argv
import sqlite3
from utilities import *
from collections import OrderedDict

DATABASE_FILE = 'scorelib.dat'

SELECTS = {
    'person': 'select name, born, died from person where id = ?',
    'score': 'select name, genre, key, incipit, year from score where id = ?',
    'voice': 'select name, range, number from voice where score = ?',
    'edition': 'select name, score, year from edition where id = ?',
    'score_author': 'select composer from score_author where score = ?',
    'edition_author': 'select editor from edition_author where edition = ?',
    'initial': r"""
    select print.id, print.partiture, print.edition, person.name from person
    join score_author on person.id = score_author.composer
    join score on score_author.score = score.id
    join edition on score.id = edition.score
    join print on edition.id = print.edition
    where person.name like ?"""
}


def select_by(cursor, key, parameters):
    return cursor.execute(SELECTS[key], parameters).fetchall()


def person_to_json_object(name, born, died):
    object = OrderedDict()
    object["name"] = name
    if validate_value(born):
        object["born"] = born
    if validate_value(died):
        object["died"] = died
    return object


def voice_to_json_object(name, range):
    object = OrderedDict()
    if validate_value(name):
        object["name"] = name
    if validate_value(range):
        object["range"] = range
    return object


def print_to_json_object(print_number, composers, score_name, score_genre, score_year, edition_name, editors, voices, \
                         partiture, score_key, score_incipit):
    object = OrderedDict()
    object["Print Number"] = print_number
    if not_empty(composers):
        object["Composer"] = composers
    if validate_value(score_name):
        object["Title"] = score_name
    if validate_value(score_genre):
        object["Genre"] = score_genre
    if validate_value(score_year):
        object["Composition Year"] = score_year
    if validate_value(edition_name):
        object["Edition"] = edition_name
    if not_empty(editors):
        object["Editor"] = editors
    if not_empty(voices):
        object["Voices"] = voices
    if validate_value(partiture):
        object["Partiture"] = partiture
    if validate_value(score_key):
        object["Key"] = score_key
    if validate_value(score_incipit):
        object["Incipit"] = score_incipit
    return object


def fill_from_query(query_result, cursor, composer_substring):
    substring_pattern = '%{}%'.format(composer_substring)
    for print_row in select_by(cursor, 'initial', (substring_pattern,)):
        composer_query = print_row[3]

        print_number = print_row[0]
        partiture = True if (print_row[1] == 'Y') else False
        edition_id = print_row[2]

        edition_row = select_by(cursor, 'edition', (edition_id,))[0]
        edition_name = edition_row[0]
        score_id = edition_row[1]

        editors = []
        for editor_row in select_by(cursor, 'edition_author', (edition_id,)):
            for person in select_by(cursor, 'person', (editor_row[0],)):
                editors.append(person_to_json_object(person[0], person[1], person[2]))

        score_row = select_by(cursor, 'score', (score_id,))[0]
        score_name = score_row[0]
        score_genre = score_row[1]
        score_key = score_row[2]
        score_incipit = score_row[3]
        score_year = score_row[4]

        composers = []
        for score_author_row in select_by(cursor, 'score_author', (score_id,)):
            for person in select_by(cursor, 'person', (score_author_row[0],)):
                composers.append(person_to_json_object(person[0], person[1], person[2]))

        voices = OrderedDict()
        for voice_row in select_by(cursor, 'voice', (score_id,)):
            voices[voice_row[2]] = voice_to_json_object(voice_row[0], voice_row[1])

        print = print_to_json_object(print_number, composers, score_name, score_genre, score_year, edition_name, \
                                     editors, voices, partiture, score_key, score_incipit)

        if not composer_query in query_result:
            query_result[composer_query] = []
        query_result[composer_query].append(print)


def main():
    if len(argv) != 2:
        raise ValueError('Wrong number of arguments passed')
    composer_substring = argv[1]

    connection = db_connect(DATABASE_FILE)
    cursor = connection.cursor()

    query_result = OrderedDict()
    fill_from_query(query_result, cursor, composer_substring)

    print_nice_json(query_result)

    connection.close()


if __name__ == '__main__':
    main()
