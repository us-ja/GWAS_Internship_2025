import sys
sys.path.append('..')
import random
from my_utils import *
res=[]
def givepers(l:int, sel_pers:list=[], fileprefix="blood_lipid"):
    k=get_total_pers(fileprefix=fileprefix)
    if sel_pers==[]:
        return list(range(l%4*int(0.225*k), (l%4+1)*int(0.225*k)))
    else:
        return sel_pers[l%4*int(0.225*k):(l%4+1)*int(0.225*k)]
print(get_total_snp("blood_lipid"), get_total_pers("blood_lipid"))
seed=100
print("start with seed", seed, "at", curr_time())
random.seed(seed)
sel_pers=(list(range(get_total_pers("blood_lipid"))))
random.shuffle(sel_pers)
print(sel_pers)
comm="25_s"+str(seed)
res.append(combine_build_up(300, "blood_lipid",add_comm=comm, seed=seed, sel_pers=sel_pers,change_pers_func=givepers, checkdoubles=False,shuffle_in_level=True, total_snp=1000))

for e in res:
    print("\n Analysis of ",e)
    compare(e, "blood_lipid")
print("finished all at", curr_time())