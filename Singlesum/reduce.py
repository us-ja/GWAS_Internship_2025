import sys
sys.path.append('..')
import subprocess
import random 
import numpy as np
from datetime import datetime
import os  
from my_utils import *
fileprefix="HapMap"


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





accept_pers=[41, 7, 32, 105, 102, 86, 23, 29, 63, 58, 49, 78, 55, 94, 95, 50, 84, 12, 18, 21, 107, 20, 37, 42, 73]
individual=[]
for h in range(total_pers):
    line=ped_lines[h]
    individual.append(line.split('\t'))


good_snps=[]
for num in range(total_snp):
    
    if is_good_snp(num, individual, b_lines=b_lines, total_pers=total_pers, accept_pers=accept_pers):
        good_snps.append(num)
print(len(good_snps))  
for e in [-519947.5, -633001.5, -555449.5, -986074, -212751, -223882, -468532, -497870]:

    print(is_good_snp(int(abs(e)),individual, b_lines=b_lines, total_pers=total_pers, print_reas=True, accept_pers=accept_pers))
print(is_good_snp(555449,individual, b_lines=b_lines, total_pers=total_pers, print_reas=True))
# conversion(good_snps,"given", "goodones", 6, fileprefix)

