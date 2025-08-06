import sys
sys.path.append('..')
import random
from my_utils import *
res=[]
fileprefix="HapMap"


hap=open("HapMap.ped")
l=hap.readlines()
hap.close()





for seed in range(200, 205):
    ids=[]
    ref=l[1].split("\t")[seed]
    for line in l:
        var=line.split("\t")
        if int(var[5])==2 or (var[seed])==ref:
            ids.append(var[1])  
    grouping25(fileprefix, seed, 200, plines=l, change_pheno=(lambda x: 1 if x in ids else 0) )