import json


def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def create_json(dico, path):
    name_field=(path.rstrip('.json')).lstrip('Instances/')

    with open(f'SOL/{name_field}-sol_11.json', 'w') as f:
        json.dump(dico, f, indent=2)
    return



