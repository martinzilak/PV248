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
    'print': 'insert into print(id, partiture, edition) values (?, ?, ?)'
}
SELECTS = {
    'person': 'select id from person where name = ?',
    'score': 'select id from score where name = ? and genre = ? and key = ? and incipit = ? and year = ?',
    'voice': 'select id from voice where name = ? and number = ? and score = ? and range = ?',
    'edition': 'select id from edition where name = ? and score = ? and year = ?',
    'score_author': 'select id from score_author where score = ? and composer = ?',
    'edition_author': 'select id from edition_author where edition = ? and editor = ?',
    'print': 'select id from print where id = ? and partiture = ? and edition = ?'
}


def insert_person(cur, name, born, died):
    cur.execute(SELECTS['person'], (name,))
    data = cur.fetchone()
    if data is None:
        cur.execute(INSERTS['person'], (name, born, died,))
        return cur.lastrowid
    else:
        return data[0]


def insert_into(table, cur, params):
    cur.execute(SELECTS[table], params)
    data = cur.fetchone()
    if data is None:
        cur.execute(INSERTS[table], params)
        return cur.lastrowid
    else:
        return data[0]


def insert_score(cur, name, genre, key, incipit, year):
    return insert_into('score', cur, (name, genre, key, incipit, year,))


def insert_voice(cur, name, number, score, range):
    return insert_into('voice', cur, (name, number, score, range,))


def insert_edition(cur, name, score, year):
    return insert_into('edition', cur, (name, score, year,))


def insert_score_author(cur, score, composer):
    return insert_into('score_author', cur, (score, composer,))


def insert_edition_author(cur, edition, editor):
    return insert_into('edition_author', cur, (edition, editor,))


def insert_print(cur, id, partiture, edition):
    return insert_into('print', cur, (id, partiture, edition,))


def db_connect(db_path):
    con = sqlite3.connect(db_path)
    return con


def persist(cur, p):
    comp = p.composition()
    s_id = insert_score(cur, comp.name, comp.genre, comp.key, comp.incipit, comp.year)
    sa_id = []
    for author in comp.authors:
        per_id = insert_person(cur, author.name, author.born, author.died)
        sa_id.append(insert_score_author(cur, s_id, per_id))
    v_id = []
    for num in range(len(comp.voices)):
        v_id.append(insert_voice(cur, comp.voices[num].name, num, s_id, comp.voices[num].range))
    e_id = insert_edition(cur, p.edition.name, s_id, None)
    ea_id = []
    for author in p.edition.authors:
        per_id = insert_person(cur, author.name, author.born, author.died)
        ea_id.append(insert_edition_author(cur, e_id, per_id))
    p_id = insert_print(cur, p.print_id, 'Y' if p.partiture else 'N', e_id)


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

    for p in scorelib.load(argv[1]):
        persist(cur, p)

    con.commit()
    con.close()


if __name__ == '__main__':
    main()
