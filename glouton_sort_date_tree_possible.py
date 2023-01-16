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
    task1, date1, weight_job1 = task_date_job1
    task2, date2, weight_job2 = task_date_job2
    if date1 < date2:
        return -1
    elif date1 > date2:
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
    Bi_possible,Mi_possible,Oi_possible=[Bi],[Mi],[Oi]
    Mtm = []
    for m in range(M):
        Mtm.append([])
    Oto = []
    for o in range(O):
        Oto.append([])
    Mtm_possible,Oto_possible=[Mtm],[Oto]
    Tasks_date_job, S_associate = [[i, 0, -1] for i in range(I)], [0] * I,
    for j in range(J):
        for k, i in enumerate(S[j]):
            Tasks_date_job[i][2] = 0.7*M_space[i].count(0) + 0.1*sum(len(O_space_2d[i][m]) for m in range(M))
            if k == 0:
                Tasks_date_job[i][1] = r[i]
            else:
                Tasks_date_job[i][1] = Tasks_date_job[S[j][k - 1]][1] + p[S[j][k - 1]]
            S_associate[i] = S[j].copy()

    Tasks_date_job_sort = sorted(Tasks_date_job, key=functools.cmp_to_key(compare))
    Tasks, date = [0] * I, [0] * I
    sort_s_associate = [0] * I
    Table_coresp = [0] * I
    for i in range(I):
        Tasks[i]=Tasks_date_job_sort[i][0]
        date[i]=Tasks_date_job_sort[i][1]
        sort_s_associate[i] = S_associate[Tasks[i]]
        Table_coresp[Tasks[i]] = i
    date_possible=[date.copy()]
    for k, task in enumerate(Tasks):
        nb_possible=len(Mtm_possible)
        possibilities = operator_machine_for_task(task, O_space_2d)
        start_date_possibilities_possible = [0]*nb_possible
        start_possible = [np.inf]*nb_possible
        o_start_possible, m_start_possible = [possibilities[0][0]]*nb_possible,[possibilities[0][1]]*nb_possible
        for l in range(nb_possible):
            start_date_possibilities_possible[l]=[]
            for (o, m) in possibilities:
                start_date_possibilities_possible[l].append(start_for_task(o, m, task, date[k], Mtm_possible[l], Oto_possible[l], p))
                if start_possible[l] > start_date_possibilities_possible[l][-1]:
                    start_possible[l] = start_date_possibilities_possible[l][-1]
                    o_start_possible[l], m_start_possible[l] = o, m
                for i in range (len(start_date_possibilities_possible[l])):
                    if start_possible[l] == start_date_possibilities_possible[l][i] and nb_possible<1000:
                        start_possible.append(start_date_possibilities_possible[l][i])
                        o_start_possible.append(possibilities[i][0])
                        m_start_possible.append(possibilities[i][1])
                        Bi_possible.append(Bi_possible[l].copy())
                        Mi_possible.append(Mi_possible[l].copy())
                        Oi_possible.append(Oi_possible[l].copy())
                        Mtm_possible.append([Mtm_possible[l][i].copy() for i in range (len(Mtm_possible[l]))])
                        Oto_possible.append([Oto_possible[l][i].copy() for i in range (len(Oto_possible[l]))])
                        date_possible.append(date_possible[l].copy())
        for l in range(len(Mtm_possible)):
            c = False
            index = 0
            for l, task_same_job in enumerate(sort_s_associate[k]):
                if task_same_job == task:
                    c = True
                    index = l
                    date_possible[l][k] = start_possible[l]
                if c:
                    date_possible[l][Table_coresp[task_same_job]] = start_possible[l] + sum(p[i] for i in sort_s_associate[k][index:l])
            Bi_possible[l][task], Oi_possible[l][task], Mi_possible[l][task] = start_possible[l], o_start_possible[l], m_start_possible[l]
            bisect.insort(Mtm_possible[l][m_start_possible[l]], [start_possible[l], start_possible[l] + p[task]])
            bisect.insort(Oto_possible[l][o_start_possible[l]], [start_possible[l], start_possible[l] + p[task]])
    print("here")
    sol=analysis_sol.Solution(Bi_possible[0],Mi_possible[0],Oi_possible[0])
    for l in range(len(Mtm_possible)):
        if analysis_sol.cost(sol,INSTANCE[type_data])>analysis_sol.cost(analysis_sol.Solution(Bi_possible[l],Mi_possible[l],Oi_possible[l]),INSTANCE[type_data]):
            sol=analysis_sol.Solution(Bi_possible[l],Mi_possible[l],Oi_possible[l])
    return sol


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
        if analysis_sol.cost(SOL_GLOUTON_SORT[type_data[k]], INSTANCE[type_data[k]])<analysis_sol.cost(analysis_sol.read_solution(path[k]),INSTANCE[type_data[k]]):
            tools_json.solution_create_field(SOL_GLOUTON_SORT[type_data[k]], f'glouton_sort_date/KIRO-{type_data[k]}')
        print(analysis_sol.is_feasible(SOL_GLOUTON_SORT[type_data[k]], INSTANCE[type_data[k]]))

    COST_GLOUTON_SORT = {i: analysis_sol.cost(SOL_GLOUTON_SORT[i], INSTANCE[i]) for i in SOL_GLOUTON_SORT.keys()}
    COST_TOTAL_GLOUTON_SORT = sum(COST_GLOUTON_SORT[i] for i in COST_GLOUTON_SORT.keys())
    pprint(COST_GLOUTON_SORT)
    print(COST_TOTAL_GLOUTON_SORT)
