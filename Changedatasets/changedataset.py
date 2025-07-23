import sys
sys.path.append('..')
import random
from my_utils import *
seed=10
random.seed(seed)
def givepers(l:int):
    return list(range(l*25, (l+1)*25))


comb_res=(combine_build_up(200, "HapMap",add_comm="25per_l", seed=seed, change_pers_func=givepers, allow_unknowns=20))