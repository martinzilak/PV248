#!/usr/bin/env python

from sys import argv
import scorelib
import sqlite3
import os

TABLES = 'scorelib.sql'

INSERTS = {
    'person': 'insert into person(name, born, died) values (?, ?, ?)',
    'score': 'insert into score(name, genre, key, incipit, year) values (?, ?, ?, ?, ?)',
    'voice': 'insert into voice(name, number, score, range) values (?, ?, ?, ?)',
    'edition': 'insert into edition(name, score, year) values (?, ?, ?)',
    'score_author': 'insert into score_author(score, composer) values (?, ?)',
    'edition_author': 'insert into edition_author(edition, editor) values (?, ?)',
    'print': 'insert into print(partiture, edition) values (?, ?)'
}
SELECTS = {
    'person': 'select id from person where name = ?',
    'score': 'select id from score where name = ? and genre = ? and key = ? and incipit = ? and year = ?',
    'voice': 'select id from voice where name = ? and number = ? and score = ? and range = ?',
    'edition': 'select id from edition where name = ? and score = ? and year = ?',
    'score_author': 'select id from score_author where score = ? and composer = ?',
    'edition_author': 'select id from edition_author where edition = ? and editor = ?',
    'print': 'select id from print where partiture = ? and edition = ?'
}


def insert_person(cur, con, name, born, died):
    cur.execute(SELECTS['person'], (name,))
    data = cur.fetchone()
    if data is None:
        cur.execute(INSERTS['person'], (name, born, died,))
        con.commit()
        return cur.lastrowid
    else:
        return data[0]


def insert_into(table, cur, con, params):
    cur.execute(SELECTS[table], params)
    data = cur.fetchone()
    if data is None:
        cur.execute(INSERTS[table], params)
        con.commit()
        return cur.lastrowid
    else:
        return data[0]


def insert_score(cur, con, name, genre, key, incipit, year):
    insert_into('score', cur, con, (name, genre, key, incipit, year,))


def insert_voice(cur, con, name, number, score, range):
    insert_into('voice', cur, con, (name, number, score, range,))


def insert_edition(cur, con, name, score, year):
    insert_into('edition', cur, con, (name, score, year,))


def insert_score_author(cur, con, score, composer):
    insert_into('score_author', cur, con, (score, composer,))


def insert_edition_author(cur, con, edition, editor):
    insert_into('edition_author', cur, con, (edition, editor,))


def insert_print(cur, con, partiture, edition):
    insert_into('print', cur, con, (partiture, edition,))


def db_connect(db_path):
    con = sqlite3.connect(db_path)
    return con


def persist(cur, con, p):
    pass


def main():
    if len(argv) != 3:
        raise ValueError('Wrong number of arguments passed')
    dat = argv[2]

    if os.path.isfile(dat):
        os.remove(dat)

    con = db_connect(dat)
    cur = con.cursor()

    tables = open(TABLES).read()
    cur.executescript(tables)
    con.commit()

    for p in scorelib.load(argv[1]):
        persist(cur, con, p)


if __name__ == '__main__':
    main()
