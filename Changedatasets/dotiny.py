import sys
sys.path.append('..')
import random
from my_utils import *
fileprefix="HapMap"
print("Start at", curr_time())
for seed in range(400, 415):
    grouping(fileprefix,seed,80,add_comm="tiny")
print("finished at", curr_time())