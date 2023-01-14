import json


def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def solution_create_field(solution, path):
    sol = []
    I = len(solution.starts)
    for i in range(I):
        sol.append({'task': i + 1, 'start': solution.starts[i], 'machine': solution.machines[i] + 1, 'operator': solution.operators[i] + 1})
    name_field = (path.rstrip('.json')).lstrip('Instances/')
    with open(f'SOL/{name_field}-sol_11.json', 'w') as f:
        json.dump(sol, f, indent=2)
