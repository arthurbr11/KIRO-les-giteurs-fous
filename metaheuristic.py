import numpy as np
import bisect
import collections
import itertools
from tqdm import tqdm

import extract_data
import tools_json
import analysis_sol
import glouton
import space_sol

SPACE_SOL = tools_json.space_sol_read_fieald()
