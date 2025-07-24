import sys
sys.path.append('..')
import random
from my_utils import *
seed=10
random.seed(seed)

a_pers=(random.sample(range(0,109), k= int(0.9*109)))
a_pers.sort()


comm="9fold_s"+str(seed)
comb_res=(combine_build_up(200, "HapMap", sel_pers=a_pers, add_comm=comm, seed=seed))



