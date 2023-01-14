import numpy as np
import bisect
import collections
import itertools
from tqdm import tqdm
from pprint import pprint
import extract_data
import tools_json
import analysis_sol
import glouton

INSTANCE = glouton.INSTANCE
def born_inf(type_data):
    born=0
    for job in INSTANCE[type_data].jobs:
        s=0
        for i in job.task_sequence:
            s+=INSTANCE[type_data].tasks[i].processing_time
        born+=job.weight*(job.release_date+s)
    return born
BORN={'tiny': born_inf('tiny'),'small': born_inf('small'),'medium': born_inf('medium'),'large': born_inf('large')}

BORN_TOTAL= sum(i for i in BORN.values())
print(BORN)
print(BORN_TOTAL)