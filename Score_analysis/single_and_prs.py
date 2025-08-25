
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


member_snps=[]
ped_file=(fileprefix+".ped")
bed_file=(fileprefix+".bim")
total_snp=get_total_snp(fileprefix)
total_pers=get_total_pers(fileprefix)


ped= open(ped_file) 
ped_lines = ped.readlines()
ped.close()
bim= open(bed_file) 
b_lines = bim.readlines()
bim.close()
individual=[]
for h in range(total_pers):
    line=ped_lines[h]
    individual.append(line.split('\t'))
good_snps=[]
for num in range(total_snp):
    
    if is_good_snp(num, individual, b_lines=b_lines, total_pers=total_pers):
        good_snps.append(num)
j=0
i=0

while i < 1000:

    while not is_good_snp(sorted[j][1], individual, b_lines, total_pers):
        print("skip", sorted[j][1])
        j+=1
    print(i,j, sorted[j][1], "add")
    member_snps.append(sorted[j][1])
    i+=1
    j+=1

print(curr_time())
res_out=conversion(member_snps, "given", "tuned", 8,fileprefix=fileprefix,delete_logs=True, allow_unknowns=30, stopifoverspecif=True)
print(res_out, curr_time())
