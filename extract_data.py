import tools_json
from pprint import pprint
'Instances/tiny.json'
def return_all_parameters(path):
    brut_data = tools_json.read_json(path)

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

    """ Tasks i parameters and machines m in M_spaces[i] parameters"""
    p = []
    M_space = []
    O_space=[]#Oim=O[i][m]
    for i in range(I):
        p.append(brut_data['tasks'][i]['processing_time'])
        Mi=[]
        Oi=[[]]*M
        for m in range(len(brut_data['tasks'][i]['machines'])):
            index_machines=brut_data['tasks'][i]['machines'][m]['machine']
            Mi.append(index_machines-1)
            Oi[index_machines-1]=brut_data['tasks'][i]['machines'][m]['operators']
        O_space.append(Oi)
        M_space.append(Mi)

    return (J,I,M,O,alpha,beta,S,r,d,w,p,M_space,O_space)



