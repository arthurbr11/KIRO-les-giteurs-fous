import json
from pprint import pprint


def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def create_json(dico, name_field):
    with open(f'{name_field}.json', 'w') as f:
        json.dump(dico, f, indent=2)
    return


"""data = read_json('Instances/KIRO-tiny.json')
pprint(data)
create_json(data, 'new_field')"""
