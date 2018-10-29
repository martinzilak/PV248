#!/usr/bin/env python

from sys import argv
import numpy as np
from collections import OrderedDict


def validate_value(value):
    if value is None:
        return False
    if not len(str(value)) > 0:
        return False
    return True


def parse_equation(line, coef_by_param, results, parameters):
    if validate_value(line):
        (equation, result) = line.split('=')
        pairs = OrderedDict()
        new_variable = True
        previous_symbol = '+'
        for pair in equation.split():
            pair = pair.strip()
            if new_variable:
                if pair[-1] not in parameters:
                    parameters.append(pair[-1])
                pairs[pair[-1]] = (int(pair[:-1]) if len(pair) > 1 else 1) * (1 if previous_symbol == '+' else -1)
                new_variable = False
                previous_symbol = '+'
            else:
                previous_symbol = pair
                new_variable = True

    coef_by_param.append(pairs)

    # if len(equations) < len(pairs.keys()):
    #     for i in range(len(pairs.keys()) - len(equations)):
    #         equations.append([])
    #
    # for index, (key, value) in enumerate(pairs.items()):
    #     if index == parameters.index(key):
    #         equations[parameters.index(key)].append(value)
    #     else:
    #         equations[index].append(0)
    #
    results.append(result.strip())


def build_matrixes(coef_by_param, results, parameters):
    A = []
    B = []

    for index, item in enumerate(coef_by_param):
        A.append([])
        for inner_index, (key, value) in enumerate(item.items()):
            if inner_index == parameters.index(key):
                A[index].append(value)
            else:
                A[index].append(0)

    B = results.copy()

    return A, B


def main():
    if len(argv) != 2:
        raise ValueError('Wrong number of arguments passed')
    input_file = argv[1]

    coef_by_param = []
    results = []
    parameters = []

    with open(input_file, errors='ignore') as file:
        for line in file:
            parse_equation(line, coef_by_param, results, parameters)

    A, B = build_matrixes(coef_by_param, results, parameters)

    print(A, B)


if __name__ == '__main__':
    main()
