import numpy as np
import bisect
import collections
import itertools
from tqdm import tqdm
from pprint import pprint

import extract_data
import tools_json
import analysis_sol
import glouton
import space_sol

INSTANCE = glouton.INSTANCE


def extract_space():
    SPACE_SOL = tools_json.space_sol_read_fieald()
    path = ['SOL/glouton_random/KIRO-tiny-sol_11.json', 'SOL/glouton_random/KIRO-small-sol_11.json',
            'SOL/glouton_random/KIRO-medium-sol_11.json', 'SOL/glouton_random/KIRO-large-sol_11.json']
    type_data = ['tiny', 'small', 'medium', 'large']
    for k in range(4):
        SPACE_SOL[type_data[k]].append(analysis_sol.read_solution(path[k]))
    return SPACE_SOL['tiny'].copy(), SPACE_SOL['small'].copy(), SPACE_SOL['medium'].copy(), SPACE_SOL['large'].copy()


space_sol_tiny, space_sol_small, space_sol_medium, space_sol_large = extract_space()


def caracteristic_space(space_sol, instance):
    avg = 0
    best = np.infty
    worst = 0
    for s in space_sol:
        c = analysis_sol.cost(s, instance)
        avg += c / len(space_sol)
        if c < best:
            best = c
        if c > worst:
            worst = c
    return {'nb': len(space_sol), 'best': best, 'avg': int(avg), 'worst': worst}


pprint(caracteristic_space(space_sol_tiny, INSTANCE['tiny']))
pprint(caracteristic_space(space_sol_small, INSTANCE['small']))
pprint(caracteristic_space(space_sol_medium, INSTANCE['medium']))
pprint(caracteristic_space(space_sol_large, INSTANCE['large']))
