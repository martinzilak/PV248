#!/usr/bin/env python

import json
from sys import argv
import numpy as np
import csv
from datetime import datetime, date
import math
from collections import OrderedDict


START_DATE_STRING = '2018-09-17'
DATE_FORMAT = '%Y-%m-%d'


def parse_row(headers, row_to_parse):
    output = {}

    points_by_date = {}
    points_by_exercise = {}

    for _date, points in zip(headers['dates'], row_to_parse):
        ord_date = datetime.strptime(_date, DATE_FORMAT).date().toordinal()
        if ord_date in points_by_date:
            points_by_date[ord_date] += points
        else:
            points_by_date[ord_date] = points

    for exercise, points in zip(headers['exercises'], row_to_parse):
        if exercise in points_by_exercise:
            points_by_exercise[exercise] += points
        else:
            points_by_exercise[exercise] = points

    total = 0
    passed = 0
    values = []

    for value in points_by_exercise.values():
        total += value
        if value > 0:
            passed += 1
        values.append(value)

    values.sort()

    start_date = datetime.strptime(START_DATE_STRING, DATE_FORMAT).date().toordinal()

    dates = []
    points = []

    ordered_points_by_date = OrderedDict(sorted(points_by_date.items()))

    for key, value in ordered_points_by_date.items():
        dates.append([key - start_date])
        points.append(value)

    for i in range(1, len(points)):
        points[i] += points[i - 1]

    regression_slope = np.linalg.lstsq(dates, points, rcond=-1)[0][0]

    output['total'] = total
    output['passed'] = passed
    output['mean'] = np.mean(values)
    output['median'] = np.median(values)
    output['regression slope'] = regression_slope

    if regression_slope != 0:
        output['date 16'] = date.fromordinal(math.ceil((16.0 / regression_slope) + start_date)).strftime(DATE_FORMAT)
        output['date 20'] = date.fromordinal(math.ceil((20.0 / regression_slope) + start_date)).strftime(DATE_FORMAT)

    return json.dumps(output, indent=4, ensure_ascii=False)


def parse_csv(csv_reader, input_param):
    headers = {'exercises': [], 'dates': []}
    row_to_parse = []

    columns = []

    for row_index, row in enumerate(csv_reader):
        if row_index == 0:
            for index, cell in enumerate(row):
                if index != 0:
                    headers['dates'].append(cell[:-3])
                    headers['exercises'].append(cell[-2:])
        else:
            if input_param == 'average':
                for index, cell in enumerate(row[1:]):
                    if len(columns) > index:
                        columns[index].append(float(cell))
                    else:
                        columns.append([float(cell)])
            else:
                if row[0] == input_param:
                    for cell in row[1:]:
                        row_to_parse.append(float(cell))
                    break

    if len(row_to_parse) < 1:
        average_row = []

        for column in columns:
            average_row.append(np.mean(column))

        row_to_parse = average_row

    return parse_row(headers, row_to_parse)


def main():
    if len(argv) != 3:
        raise ValueError('Wrong number of arguments passed')
    input_file = argv[1]
    input_param = argv[2]

    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file)
        print(parse_csv(csv_reader, input_param))


if __name__ == '__main__':
    main()
