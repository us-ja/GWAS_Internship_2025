import sys
sys.path.append('..')
import random
from my_utils import *
fileprefix="blood_lipid_cleaned"



for seed in range(210, 213):
    grouping25(fileprefix, seed=seed, g_size=500, )
    