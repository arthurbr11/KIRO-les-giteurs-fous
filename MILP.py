from mip import Model, xsum, minimize, INTEGER
import extract_data

path = 'Instances/tiny.json'
J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_space = extract_data.return_all_parameters(path)

def objective(T,U,CJ,w):
    return xsum(w[j] * (CJ[j] + alpha * U[j] + beta * T[j]) for j in J)

model = Model("knapsack")

B = [model.add_var(var_type=INTEGER) for i in I]  # Liste des Bi
m = [model.add_var(var_type=INTEGER) for i in I]  # Liste des mi
o = [model.add_var(var_type=INTEGER) for i in I]  # Liste des oi

T = [model.add_var(var_type=INTEGER) for j in J]  # Liste des Tj
V = [model.add_var(var_type=INTEGER) for j in J]  # Liste des Vj
U = [model.add_var(var_type=INTEGER) for j in J]  # Liste des Uj

C = [B[i] + p[i] for i in I]
BJ = [S[j][0] for j in J]  #Liste de temps de début des jobs
CJ = [S[j][-1] for j in J] #Liste de temps de fin des jobs

model.objective = minimize(xsum(w[j] * (CJ[j] + alpha * U[j] + beta * T[j]) for j in J))


for i in range(0, I):
    model += B[i] >= 0

# TEST APPARTENANCE des mi
mBelong = []
for i in range(0, I):
    if m[i] in M_space[i]:
        mBelong.append(1)
    else:
        mBelong.append(0)

for i in range(0, I):
    model += mBelong[i] == 1

# TEST APPARTENANCE des oi
oBelong = []
for i in range(0, I):
    if o[i] in O_space[i][m[i]]:
        oBelong.append(1)
    else:
        oBelong.append(0)

for i in range(0, I):
    model += oBelong[i] == 1



BJ = [S[j][0] for j in J]  #Liste de temps de début des jobs
CJ = [S[j][-1] for j in J] #Liste de temps de fin des jobs

for j in J:
    model += BJ[j]>=r[j]

for j in J:
    for h in range(1, len(S[j])):
        model += B[S[h]]-C[S[h-1]] >= 0

for j in J:
    model += T[j] >= 0
    model += T[j] - C[j] + d[j] >= 0

for j in J:
    model += V[j]-C[j]+d[j] >= 0
    model += V[j] + C[j] - d[j] >= 0
    model += U[j] >= 0
    model += U[j] >=C[j]-d[j]+1-V[j] >=0



#test non-appartenance des Bi'
BiBelong = []
for i in I:
    for i1 in I:
        if i!=i1 and m[i]==m[i1] and o[i]==o[i1]:
            if B[i] <= B[i1] <= B[i]+p[i]-1:
                BiBelong.append(0)
            else:
                BiBelong.append(1)

for k in len(BiBelong):
    model += BiBelong[k] == 1







m.optimize()

selected = [i for i in I if B[i].x >= 0.99]
print("selected items: {}".format(selected))
