#!/usr/bin/env python

from sys import argv
import scorelib

def main():
    if len(argv) != 2:
        raise ValueError('Wrong number of arguments passed')

    for _print in scorelib.load(argv[1]):
        _print.format()

if __name__ == '__main__':
    main()
