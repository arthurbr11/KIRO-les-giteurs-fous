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

SPACE_SOL = SPACE_SOL_GLOUTON.copy()
SPACE_COST = SPACE_COST_GLOUTON.copy()
COST = glouton.COST_GLOUTON
TYPE_DATA = ['tiny', 'small', 'medium', 'large']


#############################1-heuristic#########################################
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


def Opti_glouton(type_data):
    inst = SPACE_INSTANCE[type_data]
    sol = SPACE_SOL_GLOUTON[type_data]
    cost = SPACE_COST[type_data]
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
    return sol, cost


def heuristic_1(type_data, verbose=True):
    SPACE_SOL[type_data[0]], SPACE_COST[type_data[0]] = glouton_all_init_tiny(type_data[0])
    tools_json.solution_create_field(SPACE_SOL[type_data[0]], '1-heuristic/KIRO-tiny')
    for k in range(1, 4):
        SPACE_SOL[type_data[k]], SPACE_COST[type_data[k]] = Opti_glouton(type_data[k])
        tools_json.solution_create_field(SPACE_SOL[type_data[k]], f'1-heuristic/KIRO-{type_data[k]}')
        if verbose:
            print(
                f'Le glouton {SPACE_COST_GLOUTON[type_data[0]]} et celui qu on fait {analysis_sol.cost(SPACE_SOL[type_data[0]], SPACE_INSTANCE[type_data[0]])} sur {type_data[0]}.')
    cost = sum(SPACE_COST[i] for i in SPACE_SOL.keys())
    if verbose:
        print(
            f'Le glouton {COST_GLOUTON} et celui qu on fait {cost} sur le total.')
    return cost


COST = heuristic_1(TYPE_DATA)
