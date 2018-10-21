#!/usr/bin/env python

from sys import argv
import sqlite3
from utilities import *

DATABASE_FILE = 'scorelib.dat'

SELECT_COMPOSERS_BY_PRINT_ID = """
select p.name, p.born, p.died
from print join edition on print.edition = edition.id
join score on edition.score = score.id
join score_author on score.id = score_author.score
join person p on score_author.composer = p.id
where print.id = ?"""


def composers_by_print_id(cursor, print_id):
    return cursor.execute(SELECT_COMPOSERS_BY_PRINT_ID, (print_id,)).fetchall()


def parse_fetched_composers(composers):
    composers_json = []

    for composer in composers:
        object = {}
        object["name"] = composer[0]
        if composer[1]:
            object["born"] = composer[1]
        if composer[2]:
            object["died"] = composer[2]
        composers_json.append(object)

    return composers_json


def main():
    if len(argv) != 2:
        raise ValueError('Wrong number of arguments passed')
    print_id = int(argv[1])

    connection = db_connect(DATABASE_FILE)
    cursor = connection.cursor()

    composers = composers_by_print_id(cursor, print_id)
    composers_json = parse_fetched_composers(composers)
    ordered_json = order_json(composers_json, ['name', 'born', 'died'])

    print_nice_json(ordered_json)

    connection.close()


if __name__ == '__main__':
    main()
