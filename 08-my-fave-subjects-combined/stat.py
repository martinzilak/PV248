#!/usr/bin/env python

import json
from sys import argv
import numpy as np
import csv
from enum import Enum

class Modes(Enum):
    DATES = 'dates'
    DEADLINES = 'deadlines'
    EXERCISES = 'exercises'

    @staticmethod
    def values():
        return list(map(lambda m: m.value, Modes))


def parse_csv(csv_reader, mode):
    header = []
    parsed = {}

    for index, row in enumerate(csv_reader):
        if index == 0:
            header = parse_header(row, mode)
        else:
            parse_row(header, row, index, parsed)

    return parsed


def parse_header(row, mode):
    header = []
    for index, column in enumerate(row):
        if index != 0:
            if mode == Modes.DATES.value:
                header.append(column[:-3])
            if mode == Modes.DEADLINES.value:
                header.append(column)
            if mode == Modes.EXERCISES.value:
                header.append(column[-2:])

    return header

def parse_row(header, row, index, parsed):
    index -= 1
    for key, cell in zip(header, row[1:]):
        cell = float(cell)

        if key in parsed:
            if index >= len(parsed[key]):
                parsed[key].append([cell])
            else:
                parsed[key][index].append(cell)
        else:
            parsed[key] = [[cell]]

def parse_dict_row(values):
    output = {}
    size = len(values)
    passed = 0
    summed_values = []

    for value in values:
        summed = sum(value)
        summed_values.append(summed)
        if summed > 0:
            passed += 1

    summed_values.sort()

    output['mean'] = np.mean(summed_values)
    output['median'] = np.median(summed_values)
    output['first'] = np.percentile(summed_values, 25)
    output['last'] = np.percentile(summed_values, 75)
    output['passed'] = passed

    return output


def evaluate(parsed):
    output = {}

    for (key, value) in parsed.items():
        output[key] = parse_dict_row(value)

    return json.dumps(output, indent=4, ensure_ascii=False)

def main():
    if len(argv) != 3:
        raise ValueError('Wrong number of arguments passed')
    input_file = argv[1]
    mode = argv[2]
    if mode not in Modes.values():
        raise ValueError('Unknown mode (must be one of {})'.format(Modes.values()))

    parsed = {}

    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file)
        parsed = parse_csv(csv_reader, mode)

    print(evaluate(parsed))

if __name__ == '__main__':
    main()
