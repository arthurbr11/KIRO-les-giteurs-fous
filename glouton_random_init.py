import numpy as np
import bisect
import collections
import itertools
from tqdm import tqdm

import extract_data
import tools_json
import analysis_sol
import glouton

SPACE_INSTANCE = glouton.SPACE_INSTANCE
SPACE_SOL_GLOUTON = glouton.SPACE_SOL_GLOUTON
SPACE_COST_GLOUTON = glouton.SPACE_COST_GLOUTON
COST_GLOUTON = glouton.COST_GLOUTON


def glouton_all_init_tiny(type_data):
    J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_SPACE_3d, O_SPACE_2d = extract_data.return_all_parameters(
        type_data)
    Jobs_caracteristics = [[S[i], r[i]] for i in range(J)]
    permutations_jobs_caracteristics = list(itertools.permutations(Jobs_caracteristics))

    inst = SPACE_INSTANCE[type_data]
    sol = SPACE_SOL_GLOUTON[type_data]
    cost = analysis_sol.cost(sol, inst)
    for index_perm, job_caracteristic in enumerate(permutations_jobs_caracteristics):

        Sort_S = [job_caracteristic[j][0] for j in range(J)]
        Sort_r = [job_caracteristic[j][1] for j in range(J)]

        current_sol = glouton.create_solution_glouton(type_data, Sort_S, Sort_r)
        if analysis_sol.is_feasible(current_sol, inst) and analysis_sol.cost(current_sol, inst) < cost:
            sol = current_sol
            cost = analysis_sol.cost(current_sol, inst)
    return sol, cost


def Opti_glouton(type_data, space_sol, space_cost, itteration):
    inst = SPACE_INSTANCE[type_data]
    sol = space_sol[type_data]
    cost = space_cost[type_data]
    J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_SPACE_3d, O_SPACE_2d = extract_data.return_all_parameters(
        type_data)

    current_sol = glouton.create_solution_glouton(type_data, S, r)
    if analysis_sol.is_feasible(current_sol, inst) and analysis_sol.cost(current_sol, inst) < analysis_sol.cost(sol,
                                                                                                                inst):
        cost = analysis_sol.cost(current_sol, inst)
        sol = current_sol
    Sort_S = []
    Sort_r = []
    Data_job = {}
    for j in range(J):
        Data_job[w[j]] = []
    for j in range(J):
        Data_job[w[j]].append([S[j], r[j]])
    Data_job = collections.OrderedDict(sorted(Data_job.items(), reverse=False))
    for key, values in Data_job.items():
        for k in range(len(values)):
            Sort_S.append(values[k][0])
            Sort_r.append(values[k][1])
    current_sol = glouton.create_solution_glouton(type_data, Sort_S, Sort_r)
    if analysis_sol.is_feasible(current_sol, inst) and analysis_sol.cost(current_sol, inst) < analysis_sol.cost(sol,
                                                                                                                inst):
        cost = analysis_sol.cost(current_sol, inst)
        sol = current_sol
    for _ in tqdm(range(itteration)):
        index = np.random.permutation(J)
        Sort_S = []
        Sort_r = []
        for j in range(J):
            Sort_S.append(S[index[j]])
            Sort_r.append(r[index[j]])
        current_sol = glouton.create_solution_glouton(type_data, Sort_S, Sort_r)
        if analysis_sol.is_feasible(current_sol, inst) and analysis_sol.cost(current_sol, inst) < analysis_sol.cost(sol,
                                                                                                                    inst):
            cost = analysis_sol.cost(current_sol, inst)
            sol = current_sol
    return sol, cost


def heuristic_1(space_sol_init, space_cost_init, itteration, verbose=True):
    space_sol, space_cost = {}, {}
    type_data = ['tiny', 'small', 'medium', 'large']
    space_sol[type_data[0]], space_cost[type_data[0]] = glouton_all_init_tiny(type_data[0])
    tools_json.solution_create_field(space_sol[type_data[0]], 'glouton_random/KIRO-tiny')
    if verbose:
        print(
            f'On est passé de {space_cost_init[type_data[0]]} a {space_cost[type_data[0]]} sur {type_data[0]}.')
    for k in range(1, 4):
        space_sol[type_data[k]], space_cost[type_data[k]] = Opti_glouton(type_data[k], space_sol_init, space_cost_init,itteration)
        tools_json.solution_create_field(space_sol[type_data[k]], f'glouton_random/KIRO-{type_data[k]}')
        if verbose:
            print(
                f'On est passé de {space_cost_init[type_data[k]]} a {space_cost[type_data[k]]} sur {type_data[k]}.')
    cost_init = sum(space_cost_init[i] for i in space_sol.keys())
    cost = sum(space_cost[i] for i in space_sol.keys())

    if verbose:
        print(
            f'On est passé {cost_init} et celui qu on fait {cost} sur le total.')
    return space_sol, space_cost


path = ['SOL/glouton_random/KIRO-tiny-sol_11.json', 'SOL/glouton_random/KIRO-small-sol_11.json',
        'SOL/glouton_random/KIRO-medium-sol_11.json', 'SOL/glouton_random/KIRO-large-sol_11.json']
SPACE_SOL_CURRENT = {'tiny': analysis_sol.read_solution(path[0]),
                     'small': analysis_sol.read_solution(path[1]),
                     'medium': analysis_sol.read_solution(path[2]),
                     'large': analysis_sol.read_solution(path[3])}

SPACE_COST_CURRENT = {i: analysis_sol.cost(SPACE_SOL_CURRENT[i], SPACE_INSTANCE[i]) for i in SPACE_SOL_CURRENT.keys()}
COST_CURRENT = sum(SPACE_COST_CURRENT[i] for i in SPACE_COST_CURRENT.keys())
for _ in range(1):
    SPACE_SOL_CURRENT, SPACE_COST_CURRENT = heuristic_1(SPACE_SOL_CURRENT, SPACE_COST_CURRENT, 1)

COST_CURRENT = sum(SPACE_COST_CURRENT[i] for i in SPACE_COST_CURRENT.keys())