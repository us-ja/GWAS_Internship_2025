import sys
sys.path.append('..')
import random
from my_utils import *
res=[]
fileprefix="HapMap"

choosen=34
hap=open("HapMap.ped")
l=hap.readlines()
hap.close()
ids=[]
ref=l[1].split("\t")[choosen]
for line in l:
    var=line.split("\t")
    if int(var[5])==2 or (var[choosen])==ref:
        ids.append(var[1])  



for seed in range(200, 205):
    grouping25(fileprefix, seed, 200, plines=l, change_pheno=(lambda x: 1 if x in ids else 0), )