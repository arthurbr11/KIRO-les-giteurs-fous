import numpy as np
import bisect
import collections
import itertools
from tqdm import tqdm
from pprint import pprint

import extract_data
import tools_json
import analysis_sol as a
import glouton
import space_sol

INSTANCE = glouton.INSTANCE


def random_swap_index_user(User):  # o or m
    i = np.random.randint(0,len(User))
    j = np.random.randint(0,len(User))
    while i == j or User[i] == User[j]:
        j = np.random.randint(0,len(User))
    return i, j


def random_swap_index(I):
    i = np.random.randint(0,I)
    j = np.random.randint(0,I)
    while i == j:
        j = np.random.randint(0,I)
    return i, j


def extract_space():
    SPACE_SOL = tools_json.space_sol_read_fieald()
    path = ['SOL/glouton_random/KIRO-tiny-sol_11.json', 'SOL/glouton_random/KIRO-small-sol_11.json',
            'SOL/glouton_random/KIRO-medium-sol_11.json', 'SOL/glouton_random/KIRO-large-sol_11.json']
    type_data = ['tiny', 'small', 'medium', 'large']
    for k in range(4):
        SPACE_SOL[type_data[k]].append(a.read_solution(path[k]))
        SPACE_SOL[type_data[k]] = sorted(SPACE_SOL[type_data[k]],
                                         key=lambda sol: a.cost(sol, INSTANCE[type_data[k]]))

    return SPACE_SOL['tiny'].copy(), SPACE_SOL['small'].copy(), SPACE_SOL['medium'].copy(), SPACE_SOL['large'].copy()


space_sol_tiny, space_sol_small, space_sol_medium, space_sol_large = extract_space()


def caracteristic_space(space_sol, instance):
    avg = 0
    best = np.infty
    worst = 0
    for s in space_sol:
        c = a.cost(s, instance)
        avg += c / len(space_sol)
        if c < best:
            best = c
        if c > worst:
            worst = c

    return {'nb': len(space_sol), 'best': best, 'avg': int(avg), 'worst': worst}


def mutation_swap_operator(sol, data):
    mut_sol =  a.Solution(sol.starts,sol.machines,sol.operators)
    while True:
        i, j = random_swap_index_user(sol.operators)
        mut_sol.operators[i], mut_sol.operators[j] = mut_sol.operators[j], mut_sol.operators[i]
        if a.is_feasible(mut_sol, INSTANCE[data], False):
            return mut_sol


def mutation_swap_machine(sol, data):
    mut_sol =  a.Solution(sol.starts,sol.machines,sol.operators)
    while True:
        i, j = random_swap_index_user(sol.machines)
        mut_sol.machines[i], mut_sol.machines[j] = mut_sol.machines[j], mut_sol.machines[i]
        if a.is_feasible(mut_sol, INSTANCE[data], False):
            return mut_sol


def mutation_swap_start(sol, data):
    mut_sol = a.Solution(sol.starts,sol.machines,sol.operators)
    while True:
        i, j = random_swap_index(len(sol.starts))
        mut_sol.machines[i], mut_sol.machines[j] = mut_sol.machines[j], mut_sol.machines[i]
        if a.is_feasible(mut_sol, INSTANCE[data], False):
            return mut_sol


def create_child_1p(sol_1, sol_2, data):
    I = len(sol_1.starts)
    mid = I // 2
    B1, B2, O1, O2, M1, M2 = sol_1.starts.copy(), sol_2.starts.copy(), sol_1.operators.copy(), sol_2.operators.copy(), sol_1.machines.copy(), sol_2.machines.copy()
    child_1 = a.Solution(B1[0:mid] + B2[mid:I], M1[0:mid] + M2[mid:I], O1[0:mid] + O2[mid:I])
    child_2 = a.Solution(B2[0:mid] + B1[mid:I], M2[0:mid] + M1[mid:I], O2[0:mid] + O1[mid:I])
    children = []
    if a.is_feasible(child_1, INSTANCE[data],verbose=False):
        children.append(child_1)
    if a.is_feasible(child_2, INSTANCE[data],verbose=False):
        children.append(child_2)
    return children


def generate_new_gen(space_sol_data, data):
    N = len(space_sol_data)
    new_gen = space_sol_data[0:N // 10].copy()  # 10% elite old gen
    """for _ in tqdm(range((N * 2) // 100)):  # 6% mutation on old gen
        n1, n2, n3 = np.random.randint(0,N), np.random.randint(0,N), np.random.randint(0,N)
        new_gen.append(mutation_swap_machine(space_sol_data[n2], data))
        print("hello")
        new_gen.append(mutation_swap_operator(space_sol_data[n3], data))
        print("hello")
        new_gen.append(mutation_swap_start(space_sol_data[n1], data))
        print("hello")"""
    while len(new_gen) < N:
        n1, n2 = random_swap_index(N)
        children = create_child_1p(space_sol_data[n1], space_sol_data[n2], data)
        if len(children) != 0:
            new_gen.extend(children)
            print("add")
    return new_gen


print(caracteristic_space(space_sol_large, INSTANCE['large']))
new_gen = generate_new_gen(space_sol_large, 'large')
print(caracteristic_space(new_gen, INSTANCE['large']))
