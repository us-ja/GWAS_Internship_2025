import sys
sys.path.append('..')
import random
from my_utils import *
res=[]
def givepers(l:int, sel_pers=None):
    if sel_pers==None:
        return list(range(l%2*50, (l%2+1)*50))
    else:
        return sel_pers[l%2*50:(l%2+1)*50]
for seed in range(115, 130):
    print("start with seed", seed, "at", curr_time())
    random.seed(seed)
    sel_pers=random.shuffle(list(range(109)))
    comm="alternate"+str(seed)
    res.append(combine_build_up(200, "HapMap",add_comm=comm, seed=seed, sel_pers=sel_pers,change_pers_func=givepers, checkdoubles=False))

for e in res:
    print("\n Analysis of ",e, "with seed", seed)
    compare(e)