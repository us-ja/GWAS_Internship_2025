import sys
sys.path.append('..')
import random
from my_utils import *
res=[]

hap=open("HapMap.ped")
l=hap.readlines()
hap.close()
all_id=[]
for line in l:
    var=line.split("\t")
    all_id.append(var[1])

for seed in range(174, 180):
    print("start with seed", seed, "at", curr_time())
    random.seed(seed)
    ids=random.choices(all_id, k=54)
    print(ids)
    comm="pyr_chg_ph"+str(seed)
    res.append(combine_build_up(200, "HapMap",add_comm=comm, seed=seed, checkdoubles=False, change_pheno=(lambda x: 1 if x in ids else 0)))



