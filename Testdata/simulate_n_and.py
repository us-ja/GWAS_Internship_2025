import sys
sys.path.append('..')
import random
from my_utils import *

total_snp=1000000
total_pers=309
seed=300


for prod in range(1,20):
    def_ph=list(range(1,prod+1))
    fileprefix="testdata_big"+str(len(def_ph))
    createdata(fileprefix, total_snp,total_pers,seed, def_ph)
    print("created data", curr_time())
    predic_acc=grouping(fileprefix, seed=prod, g_size=200, total_snp=1000,  controlshare=0.1)
    if predic_acc[0]==None or int(predic_acc[0][0]) != 100 or int(predic_acc[0][1]) != 100:
        print(prod, "not succesful")
        if predic_acc[1]!=None:
            file=open(predic_acc[1])
            l=file.readlines()
            file.close()


