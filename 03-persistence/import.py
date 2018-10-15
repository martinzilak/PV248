#!/usr/bin/env python

from sys import argv
from scorelib import *
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
    'print': 'select id from print where id = ? and partiture = ? and edition = ?',
    'sa_p': 'select p.id from score_author sa join person p on sa.composer = p.id where sa.score = ?',
    'v_s': 'select name, range, number from voice where score = ?'
}
UPDATES = {
    'person_born': 'update person set born = ? where id = ?',
    'person_died': 'update person set died = ? where id = ?'
}


def insert_person(cur, name, born, died):
    name = '' if name is None else name
    born = '' if born is None else born
    died = '' if died is None else died
    cur.execute(SELECTS['person'], (name,))
    data = cur.fetchone()
    if data is None:
        cur.execute(INSERTS['person'], (name, born, died,))
        return cur.lastrowid
    else:
        if born:
            cur.execute(UPDATES['person_born'], (born, data[0],))
        if died:
            cur.execute(UPDATES['person_died'], (died, data[0],))
        return data[0]


def insert_into(table, cur, params):
    parameters = []
    for p in params:
        if p is None or len(str(p).strip()) < 1:
            parameters.append('')
        else:
            parameters.append(p)
    cur.execute(SELECTS[table], parameters)
    data = cur.fetchone()
    if data is None:
        cur.execute(INSERTS[table], parameters)
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
        if len(author.name) > 0:
            per_id = insert_person(cur, author.name, author.born, author.died)
            sa_id.append(insert_score_author(cur, s_id, per_id))
    v_id = []
    for num in range(len(comp.voices)):
        v_id.append(insert_voice(cur, comp.voices[num].name, num + 1, s_id, comp.voices[num].range))
    e_id = insert_edition(cur, p.edition.name, s_id, None)
    ea_id = []
    for author in p.edition.authors:
        if len(author.name) > 0:
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

    for p in load(argv[1]):
        persist(cur, p)

    con.commit()
    con.close()


if __name__ == '__main__':
    main()
