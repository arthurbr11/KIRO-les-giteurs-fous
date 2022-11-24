import tools_json


def solution(path,Solution_solveur):
    solution={[]}

    B,M,O=Solution_solveur[0],Solution_solveur[1],Solution_solveur[2]
    I=len(B)
    for i in range(I):
        solution.append({'task':i+1,"start ":B[i],"machine ":M[i],"operator ":O[i]})

    tools_json.create_json(solution,path)
