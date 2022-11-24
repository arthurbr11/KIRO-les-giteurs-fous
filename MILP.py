from mip import Model, xsum, minimize, INTEGER
import extract_data

path = 'Instances/tiny.json'
J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_space = extract_data.return_all_parameters(path)

model = Model("knapsack")

B = [model.add_var(var_type=INTEGER) for i in I]  # Liste des Bi
m = [model.add_var(var_type=INTEGER) for i in I]  # Liste des mi
o = [model.add_var(var_type=INTEGER) for i in I]  # Liste des oi

for i in range(0, I):
    model += B[i] >= 0

Bool = []

for i in range(0,I):


model.objective = minimize(xsum(p[i] * B[i] for i in I))

m.optimize()

selected = [i for i in I if B[i].x >= 0.99]
print("selected items: {}".format(selected))
