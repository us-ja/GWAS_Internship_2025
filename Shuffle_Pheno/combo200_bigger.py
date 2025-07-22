import sys
sys.path.append('..')
import random
from my_utils import *
seed=10

def change_pheno(e):
    if "5" in e or "9" in e:
        return 1
    return 0
comb_res=(combine_build_up(200, "HapMap", add_comm="5or9", seed=seed, change_pheno=change_pheno))