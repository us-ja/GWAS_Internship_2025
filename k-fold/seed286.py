import sys
sys.path.append('..')
import random
from my_utils import *
seed=286#next one is 2941
random.seed(seed)

# a_pers=(random.sample(range(0,109), k= int(0.9*109)))
# a_pers.sort()
b_pers=[5, 16, 28, 30, 37, 42, 52, 67, 73, 93, 102]#next one is
# [13, 25, 32, 53, 59, 63, 66, 77, 82, 84, 89]
a_pers=[]
i=0
j=0
while i<109:
    if (j>=len(b_pers) or i!=b_pers[j]):
        a_pers.append(i)
    else:
        j+=1
    i+=1


comm="9fold_s"+str(seed)
comb_res=(combine_build_up(200, "HapMap", sel_pers=a_pers, add_comm=comm, seed=seed))