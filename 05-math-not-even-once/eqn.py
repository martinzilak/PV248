#!/usr/bin/env python

from sys import argv
import numpy.linalg as npl
from collections import OrderedDict


def validate_value(value):
    if value is None:
        return False
    if not len(str(value)) > 0:
        return False
    return True


def parse_equation(line, coef_by_param, results, parameters):
    if validate_value(line):
        equation, result = line.split('=')
        pairs = OrderedDict()
        split = equation.split()

        if split[0].strip() in ['+', '-']:
            new_variable = False
            previous_symbol = split[0].strip()
        else:
            new_variable = True
            previous_symbol = '+'

        for pair in split:
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
        results.append(int(result.strip()))


def build_matrices(coef_by_param, results, parameters):
    A = []
    B = []

    for index, item in enumerate(coef_by_param):
        A.append([])
        for parameter in parameters:
            A[index].append(item[parameter] if parameter in item.keys() else 0)

    B = results.copy()

    return A, B


def solve(A, B, parameters):
    coefficient_rank = npl.matrix_rank(A)
    augmented_rank = npl.matrix_rank([coefficient_line + [result] for coefficient_line, result in zip(A, B)])

    if coefficient_rank == augmented_rank:
        if coefficient_rank == len(parameters):
            return (1, npl.solve(A, B))
        else:
            return (len(parameters) - coefficient_rank, [])
    else:
        return (0, [])


def format_solution(solution, parameters):
    result = ''
    for value, parameter in zip(solution, parameters):
        result += '{} = {}, '.format(parameter, value)
    return result[:-2]


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

    parameters.sort()
    A, B = build_matrices(coef_by_param, results, parameters)

    solution_count, solution = solve(A, B, parameters)
    if solution_count == 0:
        print('no solution')
    elif solution_count == 1 and len(solution) > 0:
        print('solution: {}'.format(format_solution(solution, parameters)))
    else:
        print('solution space dimension: {}'.format(solution_count))


if __name__ == '__main__':
    main()
