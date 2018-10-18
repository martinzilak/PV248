#!/usr/bin/env python

from sys import argv
from scorelib import *
import sqlite3

TABLE_DEFINITIONS = 'scorelib.sql'

DROP_TABLE = 'drop table if exists {}'

TABLES = ['person', 'score', 'voice', 'edition', 'score_author', 'edition_author', 'print']

INSERTS = {
    'person': 'insert into person(name, born, died) values (?, ?, ?)',
    'score': 'insert into score(name, genre, key, incipit, year) values (?, ?, ?, ?, ?)',
    'voice': 'insert into voice(name, number, score, range) values (?, ?, ?, ?)',
    'edition': 'insert into edition(name, score, year) values (?, ?, ?)',
    'score_author': 'insert into score_author(score, composer) values (?, ?)',
    'edition_author': 'insert into edition_author(edition, editor) values (?, ?)',
    'print': 'insert into print(id, partiture, edition) values (?, ?, ?)'
}

UPDATES = {
    'person_born': 'update person set born = ? where id = ?',
    'person_died': 'update person set died = ? where id = ?'
}


def db_connect(database):
    return sqlite3.connect(database)


def clear_database(cursor):
    for table in TABLES:
        cursor.execute(DROP_TABLE.format(table))


def insert_into(cursor, table, parameters):
    cursor.execute(INSERTS[table], parameters)
    return cursor.lastrowid


def update_by(cursor, key, parameters):
    cursor.execute(UPDATES[key], parameters)


def valid(values):
    for value in values:
        if not value:
            return False
        if not len(str(value)) > 0:
            return False
    return True


def insert_person(cursor, person, people_map):
    if valid((person.name,)):
        if person.name not in people_map:
            people_map[person.name] = insert_into(cursor, 'person', (person.name, person.born, person.died,))
        else:
            if person.born:
                update_by(cursor, 'person_born', (person.born, people_map[person.name],))
            if person.died:
                update_by(cursor, 'person_died', (person.died, people_map[person.name],))


def insert_edition_author(cursor, edition, people_map):
    for editor in edition.authors:
        insert_person(cursor, editor, people_map)


def insert_score_author(cursor, composition, people_map):
    for composer in composition.authors:
        insert_person(cursor, composer, people_map)


def insert_score(cursor, composition, score_map, people_map):
        if composition not in score_map:
            score_map[composition] = \
                insert_into(cursor, 'score', (composition.name, composition.genre, composition.key, composition.incipit, composition.year,))

            for voice in composition.voices:
                if voice.range or len(voice.name) > 0:
                    insert_into(cursor, 'voice', (voice.name, voice.number, score_map[composition], voice.range,))

            for person in composition.authors:
                if valid((person.name,)):
                    insert_into(cursor, 'score_author', (score_map[composition], people_map[person.name],))


def insert_edition(cursor, edition, edition_map, score_map, people_map):
    if edition not in edition_map:
        edition_map[edition] = \
            insert_into(cursor, 'edition', (edition.name, score_map[edition.composition], None,))

        for person in edition.authors:
            if valid((person.name,)):
                insert_into(cursor, 'edition_author', (edition_map[edition], people_map[person.name],))


def insert_print(cursor, print, print_map, edition_map):
    if print not in print_map:
        print_map[print] = \
            insert_into(cursor, 'print', (print.print_id, 'Y' if print.partiture else 'N', edition_map[print.edition],))


def persist(cursor, prints):
    people_map = {}
    score_map = {}
    edition_map = {}
    print_map = {}

    for i in range(4):
        for print in prints:
            edition = print.edition
            composition = print.composition()

            if i == 0:
                insert_edition_author(cursor, edition, people_map)
                insert_score_author(cursor, composition, people_map)

            if i == 1:
                insert_score(cursor, composition, score_map, people_map)

            if i == 2:
                insert_edition(cursor, edition, edition_map, score_map, people_map)

            if i == 3:
                insert_print(cursor, print, print_map, edition_map)


def main():
    if len(argv) != 3:
        raise ValueError('Wrong number of arguments passed')
    database = argv[2]
    entry_file = argv[1]

    connection = db_connect(database)
    cursor = connection.cursor()

    clear_database(cursor)

    tables = open(TABLE_DEFINITIONS).read()
    cursor.executescript(tables)

    persist(cursor, load(entry_file))

    connection.commit()
    connection.close()


if __name__ == '__main__':
    main()
