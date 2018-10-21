import json
from collections import OrderedDict
import sqlite3


def print_nice_json(json_data):
    print(json.dumps(json_data, indent=4, ensure_ascii=False))


def order_json(json_data, sort_order):
    return [OrderedDict(sorted(item.items(), key=lambda item: sort_order.index(item[0]))) for item in json_data]


def validate_values(values):
    for value in values:
        if value is None:
            return False
        if not len(str(value)) > 0:
            return False
    return True


def validate_value(value):
    if value is None:
        return False
    if not len(str(value)) > 0:
        return False
    return True


def not_empty(collection):
    return len(collection) > 0


def db_connect(database):
    return sqlite3.connect(database)
