import numpy as np
import bisect
import collections
import time

import extract_data
import tools_json
import analysis_sol


def not_intersect(creneau, list_creneau_taken):
    for c in list_creneau_taken:
        if c[0] <= creneau[0] <= c[1] or c[0] <= creneau[1] <= c[1]:
            return False
    return True


def operator_machine_for_task(i, O_space_2d):
    result = []
    for m in range(len(O_space_2d[i])):
        if len(O_space_2d[i][m]) != 0:
            for o in O_space_2d[i][m]:
                result.append([o, m])
    return result


def start_for_task(o, m, i, r, Mtm, Oto, p):
    list_creneau_taken_for_m = Mtm[m].copy()
    list_creneau_taken_for_o = Oto[o].copy()

    if len(list_creneau_taken_for_m) == 0:
        if len(list_creneau_taken_for_o) == 0:
            return r
        else:
            if r + p[i] < list_creneau_taken_for_o[0][0]:  # cdt bord debut
                return r
            if r >= list_creneau_taken_for_o[-1][1]:  # cdt bord fin
                return r
            start = r
            for k in range(1, len(list_creneau_taken_for_o)):
                if start + p[i] < list_creneau_taken_for_o[k][0] and start > list_creneau_taken_for_o[k - 1][1]:
                    return start
                start = max(list_creneau_taken_for_o[k][1], start)
            return max(start, list_creneau_taken_for_o[-1][1])
    else:
        if len(list_creneau_taken_for_o) == 0:
            if r + p[i] < list_creneau_taken_for_m[0][0]:  # cdt bord debut
                return r
            if r >= list_creneau_taken_for_m[-1][1]:  # cdt bord fin
                return r
            start = r
            for k in range(1, len(list_creneau_taken_for_m)):
                if start + p[i] < list_creneau_taken_for_m[k][0] and start > list_creneau_taken_for_m[k - 1][1]:
                    return start
                start = max(list_creneau_taken_for_m[k][1], start)
            return max(start, list_creneau_taken_for_m[-1][1])
        else:
            if r + p[i] < list_creneau_taken_for_m[0][0] and not_intersect([r, r + p[i]],
                                                                           list_creneau_taken_for_o):  # cdt bord debut
                return r
            if r >= list_creneau_taken_for_m[-1][1] and not_intersect([r, r + p[i]],
                                                                      list_creneau_taken_for_o):  # cdt bord fin
                return r
            start = r
            for k in range(1, len(list_creneau_taken_for_m)):
                if start + p[i] < list_creneau_taken_for_m[k][0] and start > list_creneau_taken_for_m[k - 1][1]:
                    if not_intersect([start, start + p[i]], list_creneau_taken_for_o):
                        return start
                start = max(list_creneau_taken_for_m[k][1], start)
            return max(start, list_creneau_taken_for_o[-1][1], list_creneau_taken_for_m[-1][1])


def create_solution_glouton(type_data, Sort_S=None, Sort_r=None):
    J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_space_3d, O_space_2d = extract_data.return_all_parameters(
        type_data)
    Bi, Mi, Oi = [-1] * I, [-1] * I, [-1] * I

    Mtm = []
    for m in range(M):
        Mtm.append([])
    Oto = []
    for o in range(O):
        Oto.append([])
    if (Sort_S and Sort_r) is None:
        Sort_S = []
        Sort_r = []
        Data_job = {}
        for j in range(J):
            Data_job[w[j]] = []
        for j in range(J):
            Data_job[w[j]].append([S[j], r[j]])
        Data_job = collections.OrderedDict(sorted(Data_job.items(), reverse=True))
        for key, values in Data_job.items():
            for k in range(len(values)):
                Sort_S.append(values[k][0])
                Sort_r.append(values[k][1])

    for j in range(J):
        for k, i in enumerate(Sort_S[j]):
            possibilities = operator_machine_for_task(i, O_space_2d)
            start_date_possibilities = []
            start = np.inf
            o_start, m_start = possibilities[0]
            if k == 0:
                for (o, m) in possibilities:
                    start_date_possibilities.append(start_for_task(o, m, i, Sort_r[j], Mtm, Oto, p))
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
                        start_for_task(o, m, i, Bi[Sort_S[j][k - 1]] + p[Sort_S[j][k - 1]], Mtm, Oto, p))
                    if start > start_date_possibilities[-1]:
                        start = start_date_possibilities[-1]
                        o_start, m_start = o, m
                        if start == Sort_r[j]:
                            break
                Bi[i], Oi[i], Mi[i] = start, o_start, m_start
                bisect.insort(Mtm[m_start], [start, start + p[i]])
                bisect.insort(Oto[o_start], [start, start + p[i]])
    return analysis_sol.Solution(Bi, Mi, Oi)


INSTANCE = {'tiny': analysis_sol.read_instance('Instances/KIRO-tiny.json'),
                  'small': analysis_sol.read_instance('Instances/KIRO-small.json'),
                  'medium': analysis_sol.read_instance('Instances/KIRO-medium.json'),
                  'large': analysis_sol.read_instance('Instances/KIRO-large.json')}
SOL_GLOUTON = {'tiny': create_solution_glouton('tiny'),
                     'small': create_solution_glouton('small'),
                     'medium': create_solution_glouton('medium'),
                     'large': create_solution_glouton('large')}
type_data = ['tiny', 'small', 'medium', 'large']
if __name__ == "__main__":
    for k in range(4):
        tools_json.solution_create_field(SOL_GLOUTON[type_data[k]], f'glouton/KIRO-{type_data[k]}')
        print(analysis_sol.is_feasible(SOL_GLOUTON[type_data[k]],INSTANCE[type_data[k]]))

COST_GLOUTON = {i: analysis_sol.cost(SOL_GLOUTON[i], INSTANCE[i]) for i in SOL_GLOUTON.keys()}
COST_TOTAL_GLOUTON = sum(COST_GLOUTON[i] for i in COST_GLOUTON.keys())
