import numpy as np
import bisect
import collections
import itertools
from tqdm import tqdm

import extract_data
import tools_json
import analysis_sol
import glouton

Space_instance = glouton.Space_instance
Space_sol_glouton = glouton.Space_sol_glouton
Space_cost_glouton = glouton.Space_cost_glouton
cost_glouton = glouton.cost_glouton

Space_sol = Space_sol_glouton.copy()
Space_cost = Space_cost_glouton.copy()
cost = glouton.cost_glouton


#############################1-heuristic#########################################
def glouton_all_init_tiny(type_data):
    J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_space_3d, O_space_2d = extract_data.return_all_parameters(
        type_data)
    Jobs_caracteristics = [[S[i], r[i]] for i in range(J)]
    permutations_jobs_caracteristics = list(itertools.permutations(Jobs_caracteristics))

    inst = Space_instance[type_data]
    sol = Space_sol_glouton[type_data]
    cost = analysis_sol.cost(sol, inst)
    for index_perm, job_caracteristic in enumerate(permutations_jobs_caracteristics):

        Sort_S = [job_caracteristic[j][0] for j in range(J)]
        Sort_r = [job_caracteristic[j][1] for j in range(J)]

        current_sol = glouton.create_solution_glouton(type_data, Sort_S, Sort_r)
        if analysis_sol.is_feasible(current_sol, inst) and analysis_sol.cost(current_sol, inst) < cost:
            sol = current_sol
            cost = analysis_sol.cost(current_sol, inst)
    return (sol, cost)


type_data = 'tiny'
Space_sol[type_data], Space_cost[type_data] = glouton_all_init_tiny('tiny')
tools_json.solution_create_field(Space_sol[type_data], '1-heuristique/KIRO-tiny')
print(
    f'Le glouton {Space_cost_glouton[type_data]} et celui qu on fait {analysis_sol.cost(Space_sol[type_data], Space_instance[type_data])} sur {type_data}.')


def Opti_glouton(type_data):
    inst = Space_instance[type_data]
    sol = Space_sol_glouton[type_data]
    cost = Space_cost[type_data]
    J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_space_3d, O_space_2d = extract_data.return_all_parameters(
        type_data)

    current_sol = glouton.create_solution_glouton(type_data, S,r)
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
    current_sol = glouton.create_solution_glouton(type_data, Sort_S,Sort_r)
    if analysis_sol.is_feasible(current_sol, inst) and analysis_sol.cost(current_sol, inst) < analysis_sol.cost(sol,
                                                                                                                inst):
        cost = analysis_sol.cost(current_sol, inst)
        sol = current_sol
    return (sol, cost)


type_data = 'small'
Space_sol[type_data], Space_cost[type_data] = Opti_glouton(type_data)
tools_json.solution_create_field(Space_sol[type_data], '1-heuristique/KIRO-small')
print(
    f'Le glouton {Space_cost_glouton[type_data]} et celui qu on fait {analysis_sol.cost(Space_sol[type_data], Space_instance[type_data])} sur {type_data}.')

type_data = 'medium'
Space_sol[type_data], Space_cost[type_data] = Opti_glouton(type_data)
tools_json.solution_create_field(Space_sol[type_data], '1-heuristique/KIRO-medium')
print(
    f'Le glouton {Space_cost_glouton[type_data]} et celui qu on fait {analysis_sol.cost(Space_sol[type_data], Space_instance[type_data])} sur {type_data}.')

type_data = 'large'
Space_sol[type_data], Space_cost[type_data] = Opti_glouton(type_data)
tools_json.solution_create_field(Space_sol[type_data], '1-heuristique/KIRO-large')
print(
    f'Le glouton {Space_cost_glouton[type_data]} et celui qu on fait {analysis_sol.cost(Space_sol[type_data], Space_instance[type_data])} sur {type_data}.')

cost = sum(Space_cost[i] for i in Space_sol.keys())
print(
    f'Le glouton {cost_glouton} et celui qu on fait {cost} sur le total.')


