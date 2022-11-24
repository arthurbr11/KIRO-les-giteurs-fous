from mip import Model, xsum, minimize, INTEGER
import extract_data


J, I, M, O, alpha, beta, S, r, d, w, p, M_space, O_space = extract_data.return_all_parameters(path)
def objective(T,U,C,w):
    if
    sum(w[j] * (C[j] + alpha * U[j] + beta * T[j] for j in range(J)))

