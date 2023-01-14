import numpy as np
import collections
import itertools
from tqdm import tqdm

import extract_data
import tools_json
import analysis_sol as a
import glouton

INSTANCE = glouton.INSTANCE
SOL_GLOUTON = glouton.SOL_GLOUTON
COST_GLOUTON = glouton.COST_GLOUTON
COST_TOTAL_GLOUTON = glouton.COST_TOTAL_GLOUTON


def glouton_all_init_tiny_space():
    J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_SPACE_3d, O_SPACE_2d = extract_data.return_all_parameters(
        'tiny')
    Jobs_caracteristics = [[S[i], r[i]] for i in range(J)]
    permutations_jobs_caracteristics = list(itertools.permutations(Jobs_caracteristics))

    inst = INSTANCE['tiny']
    sol = SOL_GLOUTON['tiny']
    space = [sol]
    for index_perm, job_caracteristic in enumerate(permutations_jobs_caracteristics):

        Sort_S = [job_caracteristic[j][0] for j in range(J)]
        Sort_r = [job_caracteristic[j][1] for j in range(J)]

        current_sol = glouton.create_solution_glouton('tiny', Sort_S, Sort_r)
        if a.is_feasible(current_sol, inst):
            if current_sol not in space:
                space.append(current_sol)

    return space


def Opti_glouton(type_data, space_sol, itteration):
    inst = INSTANCE[type_data]
    space = space_sol.copy()
    J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_SPACE_3d, O_SPACE_2d = extract_data.return_all_parameters(
        type_data)

    current_sol = glouton.create_solution_glouton(type_data, S, r)
    if a.is_feasible(current_sol, inst):
        if current_sol not in space[type_data]:
            space[type_data].append(current_sol)
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
    if a.is_feasible(current_sol, inst):
        if current_sol not in space[type_data]:
            space[type_data].append(current_sol)
    for _ in range(itteration):
        index = np.random.permutation(J)
        Sort_S = []
        Sort_r = []
        for j in range(J):
            Sort_S.append(S[index[j]])
            Sort_r.append(r[index[j]])
        current_sol = glouton.create_solution_glouton(type_data, Sort_S, Sort_r)
        if a.is_feasible(current_sol, inst):
            if current_sol not in space[type_data]:
                space[type_data].append(current_sol)
    return space


def glouton_random_space(space_sol, itteration, verbose=True):
    space = space_sol.copy()
    type_data = ['tiny', 'small', 'medium', 'large']
    if verbose:
        print(
            f'On a {len(space[type_data[0]])} sol realisable sur  {type_data[0]}.')
    for k in range(1, 4):
        space = Opti_glouton(type_data[k], space, itteration)
        if verbose:
            print(f'On a {len(space[type_data[k]])} sol realisable sur  {type_data[k]}.')
    tools_json.space_sol_create_fieald(SPACE_SOL)
    return space


if __name__ == 'main':
    SPACE_SOL = {'tiny': glouton_all_init_tiny_space(),
                 'small': [glouton.SOL_GLOUTON['small']],
                 'medium': [glouton.SOL_GLOUTON['medium']],
                 'large': [glouton.SOL_GLOUTON['large']]}

    for _ in tqdm(range(10)):
        SPACE_SOL = glouton_random_space(SPACE_SOL, 100, verbose=False)
