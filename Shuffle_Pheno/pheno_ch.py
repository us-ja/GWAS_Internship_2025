import sys
sys.path.append('..')
import random
from my_utils import *
res=[]

hap=open("HapMap.ped")
l=hap.readlines()
hap.close()
ids=[]
for line in l:
    var=line.split("\t")
    ids.append(var[1])

for seed in range(170, 175):
    print("start with seed", seed, "at", curr_time())
    random.seed(seed)
    ids=random.choices(ids, k=54)
    print(ids)
    comm="chg_ph_rand"+str(seed)
    res.append(combine_build_up(200, "HapMap",add_comm=comm, seed=seed, checkdoubles=False, change_pheno=(lambda x: 1 if x in ids else 0)))

for e in res:
    print("\n Analysis of ",e)
    compare(e)
print("finished all at", curr_time())