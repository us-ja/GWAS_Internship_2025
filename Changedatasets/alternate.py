import sys
sys.path.append('..')
import random
from my_utils import *
seed=10
random.seed(seed)
def givepers(l:int):
    return list(range(l%2*50, (l%2+1)*50))


comb_res=(combine_build_up(200, "HapMap",add_comm="50per_l", seed=seed, change_pers_func=givepers, allow_unknowns=20, checkdoubles=False))