import numpy as np
import bisect
import collections
import itertools

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


def glouton_all_init_tiny_small(path):
    J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_space_3d, O_space_2d = extract_data.return_all_parameters(path)
    Jobs_caracteristics = [[S[i], r[i]] for i in range(J)]
    permutations_jobs_caracteristics = list(itertools.permutations(Jobs_caracteristics))

    sol = 0
    cost = np.infty
    inst=analysis_sol.read_instance(path)
    for index_perm,job_caracteristic in enumerate(permutations_jobs_caracteristics):
        print(index_perm)
        Bi, Mi, Oi = [-1] * I, [-1] * I, [-1] * I

        Mtm = []
        for m in range(M):
            Mtm.append([])
        Oto = []
        for o in range(O):
            Oto.append([])

        Sort_S = [job_caracteristic[j][0] for j in range(J)]
        Sort_r = [job_caracteristic[j][1] for j in range(J)]

        for j in range(J):
            for k, i in enumerate(Sort_S[j]):
                possibilities = glouton.operator_machine_for_task(i, O_space_2d)
                start_date_possibilities = []
                start = np.inf
                o_start, m_start = possibilities[0]
                if k == 0:
                    for (o, m) in possibilities:
                        start_date_possibilities.append(glouton.start_for_task(o, m, i, Sort_r[j], Mtm, Oto, p))
                        if start > start_date_possibilities[-1]:
                            start = start_date_possibilities[-1]
                            o_start, m_start = o, m
                            if start == Sort_r[j]:
                                break
                    Bi[i], Oi[i], Mi[i] = start, o_start, m_start
                    bisect.insort(Mtm[m_start], [start, start + p[i]])
                    bisect.insort(Oto[o_start], [start, start + p[i]])
                else:
                    for (o, m) in possibilities:
                        start_date_possibilities.append(
                            glouton.start_for_task(o, m, i, Bi[Sort_S[j][k - 1]] + p[Sort_S[j][k - 1]], Mtm, Oto, p))
                        if start > start_date_possibilities[-1]:
                            start = start_date_possibilities[-1]
                            o_start, m_start = o, m
                            if start == Sort_r[j]:
                                break
                    Bi[i], Oi[i], Mi[i] = start, o_start, m_start
                    bisect.insort(Mtm[m_start], [start, start + p[i]])
                    bisect.insort(Oto[o_start], [start, start + p[i]])
        current_sol = analysis_sol.Solution(Bi, Mi, Oi)
        if analysis_sol.is_feasible(current_sol,inst) and analysis_sol.cost(current_sol, inst) < cost:
            sol = current_sol
            cost = analysis_sol.cost(current_sol, inst)
    return sol

sol_small = glouton_all_init_tiny_small('Instances/KIRO-small.json')
tools_json.solution_create_field(sol_small,'Instances/KIRO-small.json')

