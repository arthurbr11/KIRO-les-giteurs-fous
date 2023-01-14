import numpy as np
import bisect
import collections
import itertools
from tqdm import tqdm

import extract_data
import tools_json
import analysis_sol as a
import glouton

SPACE_INSTANCE = glouton.SPACE_INSTANCE

path = ['SOL/glouton_random/KIRO-tiny-sol_11.json', 'SOL/glouton_random/KIRO-small-sol_11.json',
        'SOL/glouton_random/KIRO-medium-sol_11.json', 'SOL/glouton_random/KIRO-large-sol_11.json']
SPACE_SOL_CURRENT = {'tiny': a.read_solution(path[0]),
                     'small': a.read_solution(path[1]),
                     'medium': a.read_solution(path[2]),
                     'large': a.read_solution(path[3])}

SPACE_COST_CURRENT = {i: a.cost(SPACE_SOL_CURRENT[i], SPACE_INSTANCE[i]) for i in SPACE_SOL_CURRENT.keys()}
COST_CURRENT = sum(SPACE_COST_CURRENT[i] for i in SPACE_COST_CURRENT.keys())


def metaheuristic_plus_proche_voisin(space_sol_init, space_cost_init, itteration, verbose=True):
    space_sol, space_cost = space_sol_init.copy(), space_cost_init.copy()
    type_data = ['tiny', 'small', 'medium', 'large']
    for k in range(4):
        data = type_data[k]
        I = SPACE_INSTANCE[data].nb_tasks()
        Bi, Oi, Mi = space_sol_init[data].starts, space_sol_init[data].operators, space_sol_init[data].machines
        Task_i = sorted([i for i in range(I)], key=lambda task: Bi[task])
        Mi_sort = [Mi[Task_i[index]] for index in range(I)]
        Oi_sort = [Oi[Task_i[index]] for index in range(I)]







        current_sol = a.Solution(Bi, Mi, Oi)
        current_cost = a.cost(current_sol, SPACE_INSTANCE[data])
        if a.is_feasible(current_sol, SPACE_INSTANCE[data]) and current_cost < space_cost[data]:
            space_sol[data],space_cost[data] = current_sol,current_cost
        tools_json.solution_create_field(space_sol[data], f'1-heuristic/KIRO-{type_data[k]}')
        if verbose:
            print(
                f'On est passé de {space_cost_init[data]} a {space_cost[data]} sur {data}.')

    cost_init = sum(space_cost_init[i] for i in space_sol.keys())
    cost = sum(space_cost[i] for i in space_sol.keys())
    if verbose:
        print(
            f'On est passé {cost_init} et celui qu on fait {cost} sur le total.')
    return(space_sol,space_cost)

SPACE_SOL_CURRENT,SPACE_COST_CURRENT=metaheuristic_plus_proche_voisin(SPACE_SOL_CURRENT, SPACE_COST_CURRENT, 1)
