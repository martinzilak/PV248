#!/usr/bin/env python

from sys import argv
import sqlite3
from json_utils import *

DATABASE_FILE = 'scorelib.dat'


def db_connect(database):
    return sqlite3.connect(database)


def main():
    if len(argv) != 2:
        raise ValueError('Wrong number of arguments passed')
    composer_substring = argv[1]

    connection = db_connect(DATABASE_FILE)
    cursor = connection.cursor()

    connection.close()


if __name__ == '__main__':
    main()
