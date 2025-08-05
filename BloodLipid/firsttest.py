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


for seed in range(200, 210):
    try:
        print("start with seed", seed, "at", curr_time())
        random.seed(seed)
        sel_pers=(list(range(get_total_pers("blood_lipid"))))
        random.shuffle(sel_pers)
        print(sel_pers)
        comm="25_s"+str(seed)
        res=(combine_build_up(400, "blood_lipid",add_comm=comm, seed=seed, sel_pers=sel_pers,change_pers_func=givepers, checkdoubles=False,shuffle_in_level=True))
        if res!=None:
            print("\n Analysis of ",res, "\n out of last level:")
            compare(res, "blood_lipid", )
            print("Out of sample")
            compare(res,"blood_lipid", accept=lambda x: True if (x in sel_pers[int(0.9*get_total_pers):]) else False,  )
    except:
        print("error in seed ", seed)
print("finished all at", curr_time())