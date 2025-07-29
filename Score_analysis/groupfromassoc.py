
# import subprocess
import sys
sys.path.append('..')
# import random 
# import numpy as np
# from datetime import datetime
# import os  
# o = sys.stdout   #define std as o
from my_utils import *


fileprefix="HapMap"

prs=[]
assoc= open("adjusted_assoc_results.assoc")

a_lines=assoc.readlines()
assoc.close()
for i in range(len(a_lines)-1):
    sc=score([i], a_lines, True)
    prs.append((sc,i))
sorted= merge_sort(prs, 0, len(prs), lambda x,y: x[0]>=y[0])#lambda x,y: x[1]>=y[1])
# for e in sorted:
#     print(e)
def iterative(sorted, step_size):
    member_snps=[]
    while True:
        for i in range(step_size):
            member_snps.append(sorted[len(member_snps)][1])
        
        print(curr_time())
        res_out=conversion(member_snps, "given", "test", 8,fileprefix=fileprefix,delete_logs=True, allow_unknowns=30, stopifoverspecif=True)
        
        
        if res_out!=None:
            break


    print(res_out, curr_time())


# member_snps=[]

# for i in range(800):
#     member_snps.append(sorted[len(member_snps)][1])

# print(curr_time())
# res_out=conversion(member_snps, "given", "test", 8,fileprefix=fileprefix,delete_logs=True, allow_unknowns=30, stopifoverspecif=True)





# print(res_out, curr_time())
