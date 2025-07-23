import sys
sys.path.append('..')
import random
from my_utils import *
seed=10
random.seed(seed)

def change_pheno(e):
    if "5" in e or "9" in e:
        return 1
    return 0
print(curr_time())
comb_res=(combine_build_up(200, "HapMap", recover=dir_l(0),in_file="result", add_comm="5or9", seed=seed,allow_unknowns=20, change_pheno=change_pheno))
print(curr_time())