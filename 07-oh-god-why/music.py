#!/usr/bin/env python

from sys import argv
import numpy as np
import struct
import wave
import math


def main():
    if len(argv) != 3:
        raise ValueError('Wrong number of arguments passed')
    a_frequency = argv[1]
    input_file = argv[2]

    print('no peaks')


if __name__ == '__main__':
    main()
