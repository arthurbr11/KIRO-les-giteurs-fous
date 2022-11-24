from mip import Model, xsum, minimize, INTEGER
import extract_data

path = 'Instances/tiny.json'
J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_space = extract_data.return_all_parameters(path)


def objective(T, U, CJ, w):
    return xsum(w[j] * (CJ[j] + alpha * U[j] + beta * T[j]) for j in range(0, J))


model = Model("knapsack")

B = [model.add_var(var_type=INTEGER) for i in range(I)]  # Liste des Bi
m = [model.add_var(var_type=INTEGER) for i in range(I)]  # Liste des mi
o = [model.add_var(var_type=INTEGER) for i in range(I)]  # Liste des oi

mBelong = [model.add_var(var_type=INTEGER) for i in range(I)]  # Liste des oi
oBelong = [model.add_var(var_type=INTEGER) for i in range(I)]  # Liste des oi
BiBelong = [[model.add_var(var_type=INTEGER) for i in range(I)] for i in range(I)]
C = [model.add_var(var_type=INTEGER) for j in range(I)]

T = [model.add_var(var_type=INTEGER) for j in range(J)]  # Liste des Tj
V = [model.add_var(var_type=INTEGER) for j in range(J)]  # Liste des Vj
U = [model.add_var(var_type=INTEGER) for j in range(J)]  # Liste des Uj

BJ = [model.add_var(var_type=INTEGER) for j in range(J)]
CJ = [model.add_var(var_type=INTEGER) for j in range(J)]

model.objective = minimize(xsum(w[j] * (CJ[j] + alpha * U[j] + beta * T[j]) for j in range(J)))

for i in range(0, I):
    model += B[i] >= 0

# TEST APPARTENANCE des mi

for i in range(0, I):
    if m[i] in M_space[i]:
        model += mBelong[i] == 1
    else:
        model += mBelong[i] == 0

model += xsum(mBelong[i] for i in range(I)) == 1

# TEST APPARTENANCE des oi
for i in range(0, I):
    for machine in range(M):
        if m[i] == machine:
            if o[i] in O_space[i][machine]:
                model += oBelong[i] == 1
            else:
                model += oBelong[i] == 0

model += xsum(oBelong[i] for i in range(I)) == 1

for j in range(J):
    model += BJ[j] == S[j][0]
    model += CJ[j] == S[j][-1]

for j in range(J):
    model += BJ[j] >= r[j]

for i in range(I):
    model += C[i] - B[i] == p[i]

for j in range(J):
    for h in range(1, len(S[j])):
        model += B[S[j][h] - 1] - C[S[j][h - 1] - 1] >= 0

for j in range(J):
    model += T[j] >= 0
    model += T[j] - C[j] + d[j] >= 0

for j in range(J):
    model += V[j] - C[j] + d[j] >= 0
    model += V[j] + C[j] - d[j] >= 0
    model += U[j] >= 0
    model += U[j] >= C[j] - d[j] + 1 - V[j] >= 0

# test non-appartenance des Bi'

for i in range(I):
    for i1 in range(I):
        if i != i1 and m[i] == m[i1] and o[i] == o[i1]:
            if B[i] <= B[i1] <= B[i] + p[i] - 1:
                model += BiBelong[i][i1] == 0
            else:
                model += BiBelong[i][i1] == 1

model += xsum(xsum(BiBelong[i][j] for i in range(I)) for j in range(I)) == 1

model.optimize()
