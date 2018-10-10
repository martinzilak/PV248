#!/usr/bin/env python

from sys import argv
import scorelib
import tables
import sqlite3
import os

DATABASE = 'scorelib.dat'
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), DATABASE)
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

def insert_person(cur, name, born, died):
    cur.execute(SELECTS['person'], (name,))
    data = cur.fetchone()
    if data is None:
        cur.execute(INSERTS['person'], (name, born, died,))
        return cur.lastrowid
    else:
        return data[0]

def insert_score(cur, name, genre, key, incipit, year):
    cur.execute(SELECTS['score'], (name, genre, key, incipit, year,))
    data = cur.fetchone()
    if data is None:
        cur.execute(INSERTS['score'], (name, genre, key, incipit, year,))
        return cur.lastrowid
    else:
        return data[0]
    
def insert_voice(cur, name, number, score, range):
    cur.execute(SELECTS['voice'], (name, number, score, range,))
    data = cur.fetchone()
    if data is None:
        cur.execute(INSERTS['voice'], (name, number, score, range,))
        return cur.lastrowid
    else:
        return data[0]
    
def insert_edition(cur, name, score, year):
    cur.execute(SELECTS['edition'], (name, score, year,))
    data = cur.fetchone()
    if data is None:
        cur.execute(INSERTS['edition'], (name, score, year,))
        return cur.lastrowid
    else:
        return data[0]
    
def insert_score_author(cur, score, composer):
    cur.execute(SELECTS['score_author'], (score, composer,))
    data = cur.fetchone()
    if data is None:
        cur.execute(INSERTS['score_author'], (score, composer,))
        return cur.lastrowid
    else:
        return data[0]
    
def insert_edition_author(cur, edition, editor):
    cur.execute(SELECTS['edition_author'], (edition, editor,))
    data = cur.fetchone()
    if data is None:
        cur.execute(INSERTS['edition_author'], (edition, editor,))
        return cur.lastrowid
    else:
        return data[0]
    
def insert_print(cur, partiture, edition):
    cur.execute(SELECTS['print'], (partiture, edition,))
    data = cur.fetchone()
    if data is None:
        cur.execute(INSERTS['print'], (partiture, edition,))
        return cur.lastrowid
    else:
        return data[0]

def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con

def persist(cur, p):
    pass

def main():
    if len(argv) != 2:
        raise ValueError('Wrong number of arguments passed')

    con = db_connect()
    cur = con.cursor()

    for t in tables.tables:
        cur.execute(t)

    for p in scorelib.load(argv[1]):
        persist(cur, p)

if __name__ == '__main__':
    main()