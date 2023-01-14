import numpy as np
import bisect
import collections
import extract_data
import tools_json
import analysis_sol


def not_intersect(creneau, List_creneau_taken):
    for c in List_creneau_taken:
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


def start_for_task(o, m, i, r,Mtm,Oto,p):
    List_creneau_taken_for_m = Mtm[m].copy()
    List_creneau_taken_for_o = Oto[o].copy()

    if len(List_creneau_taken_for_m) == 0:
        if len(List_creneau_taken_for_o) == 0:
            return r+1
        else:
            if r + p[i] < List_creneau_taken_for_o[0][0]:  # cdt bord debut
                return r+1
            if r >= List_creneau_taken_for_o[-1][1]:  # cdt bord fin
                return r + 1
            start = r
            for k in range(1, len(List_creneau_taken_for_o)):
                if start + p[i] < List_creneau_taken_for_o[k][0] and start > List_creneau_taken_for_o[k - 1][1]:
                    return start
                start = max(List_creneau_taken_for_o[k][1] + 1, start)
            return max(start, List_creneau_taken_for_o[-1][1] + 1)
    else:
        if (len(List_creneau_taken_for_o) == 0):
            if r + p[i] < List_creneau_taken_for_m[0][0]:  # cdt bord debut
                return r+1
            if r >= List_creneau_taken_for_m[-1][1]:  # cdt bord fin
                return r + 1
            start = r
            for k in range(1, len(List_creneau_taken_for_m)):
                if (start + p[i] < List_creneau_taken_for_m[k][0] and start > List_creneau_taken_for_m[k - 1][1]):
                    return start
                start = max(List_creneau_taken_for_m[k][1] + 1, start)
            return max(start, List_creneau_taken_for_m[-1][1] + 1)
        else:
            if r + p[i] < List_creneau_taken_for_m[0][0] and not_intersect([r, r + p[i]], List_creneau_taken_for_o):  # cdt bord debut
                return r+1
            if r >= List_creneau_taken_for_m[-1][1] and not_intersect([r, r + p[i]], List_creneau_taken_for_o):  # cdt bord fin
                return r + 1
            start = r
            for k in range(1, len(List_creneau_taken_for_m)):
                if (start + p[i] < List_creneau_taken_for_m[k][0] and start > List_creneau_taken_for_m[k - 1][1]):
                    if (not_intersect([start, start + p[i]], List_creneau_taken_for_o)):
                        return start
                start = max(List_creneau_taken_for_m[k][1] + 1, start)
            return max(start, List_creneau_taken_for_o[-1][1] + 1,List_creneau_taken_for_m[-1][1] + 1)


def create_solution_glouton(path):
    J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_space_3d, O_space_2d = extract_data.return_all_parameters(path)
    Bi, Mi, Oi = [-1] * I, [-1] * I, [-1] * I

    Mtm = []
    for m in range(M):
        Mtm.append([])
    Oto = []
    for o in range(O):
        Oto.append([])

    Sort_S = []
    Sort_r = []
    Data_job={}
    for j in range(J):
        Data_job[f'{w[j]}']=[]
    for j in range(J):
        Data_job[f'{w[j]}'].append([S[j],r[j]])
    Data_job = collections.OrderedDict(sorted(Data_job.items()))
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
                    start_date_possibilities.append(start_for_task(o, m, i, Sort_r[j],Mtm,Oto,p))
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
                    start_date_possibilities.append(start_for_task(o, m, i, Bi[Sort_S[j][k - 1]] + p[Sort_S[j][k - 1]],Mtm,Oto,p))
                    if start > start_date_possibilities[-1]:
                        start = start_date_possibilities[-1]
                        o_start, m_start = o, m
                        if (start == Sort_r[j]):
                            break
                Bi[i], Oi[i], Mi[i] = start, o_start, m_start
                bisect.insort(Mtm[m_start], [start, start + p[i]])
                bisect.insort(Oto[o_start], [start, start + p[i]])
    return analysis_sol.Solution(Bi,Mi,Oi)


sol_tiny = create_solution_glouton('Instances/KIRO-tiny.json')
print(analysis_sol.is_feasible(sol_tiny,analysis_sol.read_instance('Instances/KIRO-tiny.json')))
tools_json.solution_create_field(sol_tiny, 'Instances/KIRO-tiny.json')

sol_small = create_solution_glouton('Instances/KIRO-small.json')
print(analysis_sol.is_feasible(sol_small,analysis_sol.read_instance('Instances/KIRO-small.json')))
tools_json.solution_create_field(sol_tiny, 'Instances/KIRO-small.json')

sol_medium = create_solution_glouton('Instances/KIRO-medium.json')
print(analysis_sol.is_feasible(sol_medium,analysis_sol.read_instance('Instances/KIRO-medium.json')))
tools_json.solution_create_field(sol_tiny, 'Instances/KIRO-medium.json')

sol_large = create_solution_glouton('Instances/KIRO-large.json')
print(analysis_sol.is_feasible(sol_large,analysis_sol.read_instance('Instances/KIRO-large.json')))
tools_json.solution_create_field(sol_tiny, 'Instances/KIRO-large.json')


