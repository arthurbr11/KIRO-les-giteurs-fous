import extract_data


def operator_machine_for_task(i,O_space_2d):
    result=[]
    for m in range(len(O_space_2d[i])):
        if len(O_space_2d[i][m])!=0:
            for o in O_space_2d[i][m]:
                    result.append([o,m])
    return result

path = 'Instances/KIRO-tiny.json'
J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_space_3d, O_space_2d = extract_data.return_all_parameters(path)
SOl = [0]*J #sol [J]{i:{start:B[i],machime m[i], operatot o[i]}} avec toutes les i task
Sort_S=[s for _, s in sorted(zip(w, S),reverse= True)]


for j in range(J):
    for i in Sort_S[j]:
        for m in range(M):
            possibility=operator_machine_for_task(i, O_space_2d)


