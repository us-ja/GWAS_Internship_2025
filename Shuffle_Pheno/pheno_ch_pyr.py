import sys
sys.path.append('..')
import random
from my_utils import *
res=[]
def givepers(l:int, sel_pers:list=[], fileprefix="HapMap"):
    k=get_total_pers(fileprefix=fileprefix)
    if sel_pers==[]:
        return list(range(l%4*int(0.25*k), (l%4+1)*int(0.25*k)))
    else:
        return sel_pers[l%4*int(0.25*k):(l%4+1)*int(0.25*k)]
hap=open("HapMap.ped")
l=hap.readlines()
hap.close()
ids=[]
for line in l:
    var=line.split("\t")
    ids.append(var[1])

for seed in range(173, 180):
    print("start with seed", seed, "at", curr_time())
    random.seed(seed)
    ids=random.choices(ids, k=54)
    print(ids)
    comm="pyr_chg_ph"+str(seed)
    res.append(combine_build_up(200, "HapMap",add_comm=comm, seed=seed, change_pers_func=givepers,checkdoubles=False, change_pheno=(lambda x: 1 if x in ids else 0)))



