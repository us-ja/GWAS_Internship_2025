import sys
sys.path.append('..')
import random
from my_utils import *
res=[]
fileprefix="testdata"

choosen=3+6

hap=open(fileprefix+".ped")
l=hap.readlines()
hap.close()




for seed in range(300, 305):
    ids=[]
    ref=l[1].split("\t")[choosen]
    for line in l:
        var=line.split("\t")
        if ("A" in (var[choosen+seed-300])):
            ids.append(var[1])  
    grouping(fileprefix, seed, 200, plines=l, change_pheno=(lambda x: 1 if x in ids else 0))