import tools_json

def solution(B,M,O,path):
    sol=[]
    I=len(B)
    for i in range(I):
        sol.append({'task':i+1,'start':B[i],'machine':M[i]+1,'operator':O[i]+1})

    tools_json.create_json(sol,path)
