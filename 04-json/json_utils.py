import json
from collections import OrderedDict


def print_nice_json(json_data):
    print(json.dumps(json_data, indent=4))


def order_json(json_data, sort_order):
    return [OrderedDict(sorted(item.items(), key=lambda item: sort_order.index(item[0]))) for item in json_data]
