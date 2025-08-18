import sys
sys.path.append('..')
import random
from my_utils import *

total_snp=1000
total_pers=109
seed=500

for mult_prod in range(1,5):
    for prod in range(1,20//mult_prod):
        print(mult_prod, prod)
        def_ph=[]
        for i in range(mult_prod):
            def_ph.append(list(range(1+i*prod,prod+1+i*prod)))
        
        fileprefix="testdata_"+str(prod+(mult_prod-1)*1000)
        createdata(fileprefix, total_snp,total_pers,seed, def_ph, mult_prod=True)
        print("created data", curr_time())
        predic_acc=grouping(fileprefix, seed=prod+(mult_prod-1)*1000, g_size=200,  controlshare=0.1, deletelog=False)
        print(predic_acc)
        if predic_acc[0]==None or int(predic_acc[0][0]) != 100 :
            print(prod, "not succesful")
            