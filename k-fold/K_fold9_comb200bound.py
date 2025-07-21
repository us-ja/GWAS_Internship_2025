import sys
sys.path.append('..')
import random
from my_utils import *
seed=10
random.seed(seed)

a_pers=(random.sample(range(0,109), k= int(0.9*109)))
a_pers.sort()

comb_res=(combine_build_up(200, "HapMap", sel_pers=a_pers, add_comm="9fold", seed=seed))
identified=set()
file=open(comb_res)
lines=file.readlines()
for i in range(-4-int(lines[1]),-4):
    ele= lines[i].split(sep=',')
    ele[0] =ele[0][1:]
    ele[-1]=ele[-1][:-2]
    ele=list(map(int, map(float, ele)))
    for j in range(len(ele)):
        identified.add(ele[j])
file.close()

def compare():
    i=0
    j=0
    b_pers=[]
    while i<109:
        if i!=a_pers[j]:
            b_pers.append(i)
        else:
            j+=1
        i+=1
    print(b_pers)
    hap= open("HapMap.ped")
    lines=hap.readlines()
    hap.close()
    risk, norisk= select_risk_al("HapMap.bim", list(map(lambda x: (int(abs(x)))+6, list(identified))))
    to_espresso(list(map(lambda x: int(abs(x))+6, (identified))), b_pers, lines, risk, norisk, "compare.txt")
    hap.close()
