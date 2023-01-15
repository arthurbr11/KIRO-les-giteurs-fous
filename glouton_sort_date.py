import numpy as np
import bisect
import collections
import time

import extract_data
import tools_json
import analysis_sol
from pprint import pprint

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


def create_solution_glouton_sort_date(type_data):
    J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_space_3d, O_space_2d = extract_data.return_all_parameters(
        type_data)
    Bi, Mi, Oi = [-1] * I, [-1] * I, [-1] * I

    Mtm = []
    for m in range(M):
        Mtm.append([])
    Oto = []
    for o in range(O):
        Oto.append([])
    Tasks,date,S_associate=[i for i in range(I)],[0]*I,[0]*I
    for j in range(J):
        for k,i in enumerate(S[j]):
            date[i]=r[j]+sum(p[l] for l in S[j][0:k])
            S_associate[i]=S[j].copy()
    Tasks=sorted(Tasks,key=lambda task: date[task])
    date=sorted(date)
    sort_s_associate=[0]*I
    for i in range(I):
        sort_s_associate[i]=S_associate[Tasks[i]]

    for k,task in enumerate(Tasks):
        if task==13 or task==17:
            d=0
        possibilities = operator_machine_for_task(task, O_space_2d)
        start_date_possibilities = []
        start = np.inf
        o_start, m_start = possibilities[0]
        for (o, m) in possibilities:
            start_date_possibilities.append(start_for_task(o, m, task, date[k], Mtm, Oto, p))
            if start > start_date_possibilities[-1]:
                start = start_date_possibilities[-1]
                o_start, m_start = o, m
        for task_same_job in sort_s_associate[k]:
            date[task_same_job] =max(start + p[task],date[task_same_job])
        Bi[task], Oi[task], Mi[task] = start, o_start, m_start
        bisect.insort(Mtm[m_start], [start, start + p[task]])
        bisect.insort(Oto[o_start], [start, start + p[task]])
    return analysis_sol.Solution(Bi, Mi, Oi)


INSTANCE = {'tiny': analysis_sol.read_instance('Instances/KIRO-tiny.json'),
                  'small': analysis_sol.read_instance('Instances/KIRO-small.json'),
                  'medium': analysis_sol.read_instance('Instances/KIRO-medium.json'),
                  'large': analysis_sol.read_instance('Instances/KIRO-large.json')}
SOL_GLOUTON_SORT = {'tiny': create_solution_glouton_sort_date('tiny'),
                     'small': create_solution_glouton_sort_date('small'),
                     'medium': create_solution_glouton_sort_date('medium'),
                     'large': create_solution_glouton_sort_date('large')}
type_data = ['tiny', 'small', 'medium', 'large']
if __name__ == "__main__":
    for k in range(4):
        tools_json.solution_create_field(SOL_GLOUTON_SORT[type_data[k]], f'glouton_sort_date/KIRO-{type_data[k]}')
        print(analysis_sol.is_feasible(SOL_GLOUTON_SORT[type_data[k]],INSTANCE[type_data[k]]))

    COST_GLOUTON_SORT = {i: analysis_sol.cost(SOL_GLOUTON_SORT[i], INSTANCE[i]) for i in SOL_GLOUTON_SORT.keys()}
    COST_TOTAL_GLOUTON_SORT = sum(COST_GLOUTON_SORT[i] for i in COST_GLOUTON_SORT.keys())
    pprint(COST_GLOUTON_SORT)
    print(COST_TOTAL_GLOUTON_SORT)