import sys
sys.path.append('..')
import random
from my_utils import *
res=[]

for seed in range(160, 165):
    print("start with seed", seed, "at", curr_time())
    random.seed(seed)
    all=(list(range(109)))
    random.shuffle(all)
    comm="pyramid"+str(seed)
    res.append(combine_build_up(200, "HapMap",add_comm=comm, seed=seed, sel_pers=all[:99],checkdoubles=False,shuffle_in_level=True))

for e in res:
    print("\n Analysis of ",e)
    compare(e)
