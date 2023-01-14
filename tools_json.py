import json
import analysis_sol


def read_json(type_data):
    with open(f'Instances/KIRO-{type_data}.json', 'r') as f:
        return json.load(f)


def solution_create_field(solution, name_field):
    sol = []
    I = len(solution.starts)
    for i in range(I):
        sol.append({'task': i + 1, 'start': solution.starts[i], 'machine': solution.machines[i] + 1,
                    'operator': solution.operators[i] + 1})
    with open(f'SOL/{name_field}-sol_11.json', 'w') as f:
        json.dump(sol, f, indent=2)


def space_sol_create_fieald(space):
    type_data = ['tiny', 'small', 'medium', 'large']
    for k in range(4):
        S = {}
        for l in range(len(space[type_data[k]])):
            solution = space[type_data[k]][l]
            sol_as_list = []
            I = len(solution.starts)
            for i in range(I):
                sol_as_list.append({'task': i + 1, 'start': solution.starts[i], 'machine': solution.machines[i] + 1,
                                    'operator': solution.operators[i] + 1})
            S[f'solution {l}'] = sol_as_list

        with open(f'SOL/space/sol-{type_data[k]}.json', 'w') as f:
            json.dump(S, f, indent=2)


def space_sol_read_fieald():
    type_data = ['tiny', 'small', 'medium', 'large']
    S = {}
    for k in range(4):
        with open(f'SOL/space/sol-{type_data[k]}.json', 'r') as f:
            data_list = json.load(f)
        S[type_data[k]] = []
        for key, data in data_list.items():

            nb_tasks = len(data)
            starts = [0] * nb_tasks
            machines = [0] * nb_tasks
            operators = [0] * nb_tasks
            for task in data:
                task_index = task["task"]
                starts[task_index - 1] = task["start"]
                machines[task_index - 1] = task["machine"] - 1
                operators[task_index - 1] = task["operator"] - 1
            S[type_data[k]].append(analysis_sol.Solution(starts, machines, operators))
    return S