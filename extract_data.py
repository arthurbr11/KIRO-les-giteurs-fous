import tools_json

def return_all_parameters(type_data):
    brut_data = tools_json.read_json(type_data)

    """Instances Parameters"""

    J = brut_data['parameters']['size']['nb_jobs']
    I = brut_data['parameters']['size']['nb_tasks']
    M = brut_data['parameters']['size']['nb_machines']
    O = brut_data['parameters']['size']['nb_operators']

    alpha = brut_data['parameters']['costs']['unit_penalty']
    beta = brut_data['parameters']['costs']['tardiness']

    """Job Parameters"""
    S = []
    r = []
    d = []
    w = []
    for j in range(J):
        S.append(brut_data['jobs'][j]['sequence'])
        r.append(brut_data['jobs'][j]['release_date'])
        d.append(brut_data['jobs'][j]['due_date'])
        w.append(brut_data['jobs'][j]['weight'])
    for k in range(len(S)):
        for l in range(len(S[k])):
            S[k][l]-=1

    """ Tasks i parameters and machines m in M_spaces[i] parameters"""
    p = []
    M_space = []
    O_space_2d=[]#Oim=O[i][m]
    for i in range(I):
        p.append(brut_data['tasks'][i]['processing_time'])
        Mi=[0]*M
        Oi=[[]]*M
        for m in range(len(brut_data['tasks'][i]['machines'])):
            index_machines=brut_data['tasks'][i]['machines'][m]['machine']
            Mi[index_machines-1]=1
            Oi[index_machines-1]=brut_data['tasks'][i]['machines'][m]['operators']
            for k in range(len(Oi[index_machines-1])):
                Oi[index_machines-1][k]-=1
        O_space_2d.append(Oi)
        M_space.append(Mi)
    O_space_3d=[]
    for i in range(I):
        Oi=[]
        for m in range(M):
            Oim=[0]*O
            for o in range(O):
                if o in O_space_2d[i][m]:
                    Oim[o]=1
            Oi.append(Oim)
        O_space_3d.append(Oi)

    return (J,I,M,O,alpha,beta,S,r,d,w,p,M_space,O_space_3d,O_space_2d)
