import numpy as np
import bisect
import collections
import time
import functools

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


def compare(task_date_job1, task_date_job2):
    task1, date1, weight_job1 , due_date1 = task_date_job1
    task2, date2, weight_job2 , due_date2 = task_date_job2
    if due_date1 < due_date2:
        return -1
    elif due_date1 > due_date2:
        return +1
    else:
        if weight_job1 >= weight_job2:
            return -1
        else:
            return +1


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
    Tasks_date_job_last_date, S_associate = [[i, 0, -1,0] for i in range(I)], [0] * I,
    for j in range(J):
        for k, i in enumerate(S[j]):
            Tasks_date_job_last_date[i][2] = d[j]
            if k == 0:
                Tasks_date_job_last_date[i][1] = r[i]
                Tasks_date_job_last_date[i][3]= d[j]-sum(p[task] for task in S[j])
            else:
                Tasks_date_job_last_date[i][1] = Tasks_date_job_last_date[S[j][k - 1]][1] + p[S[j][k - 1]]
                Tasks_date_job_last_date[i][3] = d[j]-sum(p[task] for task in S[j][k:len(S[j])])
            S_associate[i] = S[j].copy()

    Tasks_date_job_sort = sorted(Tasks_date_job_last_date, key=functools.cmp_to_key(compare))
    Tasks, date = [0] * I, [0] * I
    sort_s_associate = [0] * I
    Table_coresp = [0] * I
    for i in range(I):
        Tasks[i]=Tasks_date_job_sort[i][0]
        date[i]=Tasks_date_job_sort[i][1]
        sort_s_associate[i] = S_associate[Tasks[i]]
        Table_coresp[Tasks[i]] = i

    for k, task in enumerate(Tasks):
        possibilities = operator_machine_for_task(task, O_space_2d)
        start_date_possibilities = []
        start = np.inf
        o_start, m_start = possibilities[0]
        for (o, m) in possibilities:
            start_date_possibilities.append(start_for_task(o, m, task, date[k], Mtm, Oto, p))
            if start > start_date_possibilities[-1]:
                start = start_date_possibilities[-1]
                o_start, m_start = o, m
        c = False
        index = 0
        for l, task_same_job in enumerate(sort_s_associate[k]):
            if task_same_job == task:
                c = True
                index = l
                date[k] = start
            if c:
                date[Table_coresp[task_same_job]] = start + sum(p[i] for i in sort_s_associate[k][index:l])
            if not c:
                date[Table_coresp[task_same_job]] = start - sum(p[i] for i in sort_s_associate[k][l-1:index+1])-1
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
path = ['SOL/glouton_sort_date/KIRO-tiny-sol_11.json', 'SOL/glouton_sort_date/KIRO-small-sol_11.json',
        'SOL/glouton_sort_date/KIRO-medium-sol_11.json', 'SOL/glouton_sort_date/KIRO-large-sol_11.json']
if __name__ == "__main__":
    for k in range(4):
        tools_json.solution_create_field(SOL_GLOUTON_SORT[type_data[k]], f'glouton_sort_date/KIRO-{type_data[k]}')
        print(analysis_sol.is_feasible(SOL_GLOUTON_SORT[type_data[k]], INSTANCE[type_data[k]]))

    COST_GLOUTON_SORT = {i: analysis_sol.cost(SOL_GLOUTON_SORT[i], INSTANCE[i]) for i in SOL_GLOUTON_SORT.keys()}
    COST_TOTAL_GLOUTON_SORT = sum(COST_GLOUTON_SORT[i] for i in COST_GLOUTON_SORT.keys())
    pprint(COST_GLOUTON_SORT)
    print(COST_TOTAL_GLOUTON_SORT)