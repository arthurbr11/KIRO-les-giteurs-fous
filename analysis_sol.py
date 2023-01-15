import numpy as np
import bisect
import collections
import itertools
from tqdm import tqdm

import extract_data
import tools_json
import analysis_sol
import glouton

INSTANCE = glouton.INSTANCE
SOL_GLOUTON = glouton.SOL_GLOUTON
COST_GLOUTON = glouton.COST_GLOUTON
COST_GLOUTON = glouton.COST_TOTAL_GLOUTON


def glouton_all_init_tiny(type_data):
    J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_SPACE_3d, O_SPACE_2d = extract_data.return_all_parameters(
        type_data)
    Jobs_caracteristics = [[S[i], r[i]] for i in range(J)]
    permutations_jobs_caracteristics = list(itertools.permutations(Jobs_caracteristics))

    inst = INSTANCE[type_data]
    sol = SOL_GLOUTON[type_data]
    cost = analysis_sol.cost(sol, inst)
    for index_perm, job_caracteristic in enumerate(permutations_jobs_caracteristics):

        Sort_S = [job_caracteristic[j][0] for j in range(J)]
        Sort_r = [job_caracteristic[j][1] for j in range(J)]

        current_sol = glouton.create_solution_glouton(type_data, Sort_S, Sort_r)
        if analysis_sol.is_feasible(current_sol, inst) and analysis_sol.cost(current_sol, inst) < cost:
            sol = current_sol
            cost = analysis_sol.cost(current_sol, inst)
    return sol, cost


def Opti_glouton(type_data, sol, cost, itteration):
    inst = INSTANCE[type_data]
    sol = sol[type_data]
    cost = cost[type_data]
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
    for _ in range(itteration):
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


def glouton_random(sol_init, cost_init, itteration, verbose=True):
    sol, cost = {}, {}
    type_data = ['tiny', 'small', 'medium', 'large']
    sol[type_data[0]], cost[type_data[0]] = glouton_all_init_tiny(type_data[0])
    tools_json.solution_create_field(sol[type_data[0]], 'glouton_random/KIRO-tiny')
    if verbose:
        print(
            f'On est passé de {cost_init[type_data[0]]} a {cost[type_data[0]]} sur {type_data[0]}.')
    for k in range(1, 4):
        sol[type_data[k]], cost[type_data[k]] = Opti_glouton(type_data[k], sol_init, cost_init, itteration)
        tools_json.solution_create_field(sol[type_data[k]], f'glouton_random/KIRO-{type_data[k]}')
        if verbose:
            print(
                f'On est passé de {cost_init[type_data[k]]} a {cost[type_data[k]]} sur {type_data[k]}.')
    cost_total_init = sum(c for c in cost_init.values())
    cost_total = sum(c for c in cost.values())

    if True:  # Verbose normaly
        print(
            f'On est passé de {cost_total_init} a {cost_total} sur le total.')
    return sol, cost


if __name__ == "__main__":
    path = ['SOL/glouton_random/KIRO-tiny-sol_11.json', 'SOL/glouton_random/KIRO-small-sol_11.json',
            'SOL/glouton_random/KIRO-medium-sol_11.json', 'SOL/glouton_random/KIRO-large-sol_11.json']
    SOL_CURRENT = {'tiny': analysis_sol.read_solution(path[0]),
                   'small': analysis_sol.read_solution(path[1]),
                   'medium': analysis_sol.read_solution(path[2]),
                   'large': analysis_sol.read_solution(path[3])}

    COST_CURRENT = {i: analysis_sol.cost(SOL_CURRENT[i], INSTANCE[i]) for i in SOL_CURRENT.keys()}
    COST_TOTAL_CURRENT = sum(cost for cost in COST_CURRENT.values())
    for _ in tqdm(range(100)):
        SOL_CURRENT, COST_CURRENT = glouton_random(SOL_CURRENT, COST_CURRENT, 100, verbose=False)

    COST_TOTAL_CURRENT = sum(cost for cost in COST_CURRENT.values())
