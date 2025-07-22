import sys
sys.path.append('..')
import random
from my_utils import *
seed=10
random.seed(seed)

a_pers=(random.sample(range(0,109), k= int(0.9*109)))
a_pers.sort()

comb_res=(combine_build_up(200, "HapMap", sel_pers=a_pers, add_comm="9fold", seed=seed))



