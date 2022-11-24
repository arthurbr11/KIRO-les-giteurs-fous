import json


def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def create_json(dico, name_field):
    with open(f'{name_field}.json', 'w') as f:
        json.dump(dico, f, indent=2)
    return



