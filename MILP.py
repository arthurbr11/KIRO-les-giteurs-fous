from mip import Model, minimize, INTEGER, BINARY
import extract_data
from tqdm import tqdm

path = 'Instances/KIRO-tiny.json'
J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_space_3d, O_space_2d = extract_data.return_all_parameters(path)

THETA, Km, Ko = sum(p[i] for i in range(I)) * 5, M + 20, O + 20





model = Model("MILP")

xim = [[model.add_var(var_type=BINARY) for m in range(M)] for i in
       range(I)]  # coef xim[i][m] vaut 1 si on utilise m pour la tache i
ximo = [[[model.add_var(var_type=BINARY) for o in range(O)] for m in range(M)] for i in range(I)]  # coef ximo[i][m][o] vaut 1 si o utilise m pour la tache i

Bi = [model.add_var(var_type=INTEGER) for i in range(I)]  # List des Bi
Ci = [model.add_var(var_type=INTEGER) for i in range(I)]  # List Ci
Bj = [model.add_var(var_type=INTEGER) for j in range(J)]  # List des Bj
Cj = [model.add_var(var_type=INTEGER) for j in range(J)]  # List des Cj
Tj = [model.add_var(var_type=INTEGER) for j in range(J)]  # List des Tj
Uj = [model.add_var(var_type=BINARY) for j in range(J)]  # List des Uj
deltaii = [[model.add_var(var_type=INTEGER) for i in range(I)] for i in range(I)]
epsilonii = [[model.add_var(var_type=INTEGER) for i in range(I)] for i in range(I)]
fii = [[model.add_var(var_type=BINARY) for i in range(I)] for i in range(I)]
gii = [[model.add_var(var_type=INTEGER) for i in range(I)] for i in range(I)]
hii = [[model.add_var(var_type=INTEGER) for i in range(I)] for i in range(I)]

for i in range(I):
    for m in range(M):
        model += xim[i][m] - M_space[i][m] <= 0  # mi in Mi
        model += sum(ximo[i][m][o] for o in range(O)) - xim[i][m] == 0  # mi is the machine for o
        for o in range(O):
            model += ximo[i][m][o] + O_space_3d[i][m][o] <= 0  # o in Oi,m

for i in range(I):
    model += Ci[i] == Bi[i] + p[i]  # 2

for j in range(J):
    model += Bj[j] == Bi[S[j][0]]  # 3

for j in range(J):
    model += Cj[j] == Ci[S[j][-1]]  # 4

for j in range(J):
    model += Bj[j] >= r[j]  # 5

for j in range(J):
    for k in range(1, len(S[j])):
        model += Bi[S[j][k]] == Ci[S[j][k - 1]]  # 6

for j in range(J):
    model += Tj[j] >= Cj[j] - d[j]  # 7

for j in range(J):
    model += Uj[j]*THETA >= Tj[j]  # 8

for i1 in tqdm(range(I)):
    for i2 in range(I):
        if i1 != i2:
            model += fii[i1][i2] >= (deltaii[i1][i2] + epsilonii[i1][i2])/(Km+Ko)  # 11

            model += gii[i1][i2] >= Ci[i1] + Bi[i2]  # 12
            model += gii[i1][i2] >= -Ci[i1] - Bi[i2]

            model += hii[i1][i2] >= Bi[i1] + Bi[i2]  # 13
            model += hii[i1][i2] >= -Bi[i1] - Bi[i2]

            model += gii[i1][i2] + hii[i1][i2] - (p[i1]*(1-fii[i1][i2])) >= 0.1
            for m1 in range (M):
                for m2 in range(M):
                    model += deltaii[i1][i2] >= xim[i1][m1]*m1 - xim[i2][m2]*m2  #9
                    model += deltaii[i1][i2] >= -xim[i1][m1]*m1 + xim[i2][m2]*m2
                    for o1 in range(O):
                        for o2 in range(O):
                            model += epsilonii[i1][i2] >= ximo[i1][m1][o1] * o1 - ximo[i2][m2][o2] * o2  # 10
                            model += epsilonii[i1][i2] >= -ximo[i1][m1][o1] * o1 + ximo[i2][m2][o2] * o2


model.objective = minimize(sum(w[j] * (Cj[j] + alpha * Uj[j] + beta * Tj[j]) for j in range(J))+sum(deltaii[i1][i2]+epsilonii[i1][i2]+hii[i1][i2]+gii[i1][i2]+fii[i1][i2] if (i1 != i2) else 0 for i1 in range(I) for i2 in range(I)))

model.optimize()


