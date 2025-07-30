import sys
sys.path.append('..')
from my_utils import *
import matplotlib.pyplot as plt
import numpy as np
import os
import math

# Generate random data for the histogram

n=get_total_snp("../HapMap")
heights=[0]*n
shuffle=[0]*n

files=get_files("../", "given", "result", ["Old", "l_", "Shuffle_Pheno", "Showcase"])
# print(files)
for e in files:
    print(e)
    file=open(e)
    lines=file.readlines()
    for i in range(-4-int(lines[1]),-4):
        ele= lines[i].split(sep=',')
        ele[0] =ele[0][1:]
        ele[-1]=ele[-1][:-2]
        ele=list( map(int, map(abs,map(float, ele))))
        for e in ele:
            heights[e]+=1
    file.close()

files=get_files("../Shuffle_Pheno", "given", "result", )
# print(files)
for e in files:
    file=open(e)
    lines=file.readlines()
    for i in range(-4-int(lines[1]),-4):
        ele= lines[i].split(sep=',')
        ele[0] =ele[0][1:]
        ele[-1]=ele[-1][:-2]
        ele=list( map(int, map(abs,map(float, ele))))
        for e in ele:
            shuffle[e]+=1
    file.close()

def mybars(heights, color, label):
    first=True
    for i in range(len(heights)):
        if heights[i]!=0:
            if first:
                plt.vlines(x=i, ymin=0, ymax=heights[i], colors=color, label=label)
                first=False
            else:
                plt.vlines(x=i, ymin=0, ymax=heights[i], colors=color)
            if heights[i]>2:
                plt.text(x=i-0.01*len(heights), y=heights[i]+0.15, s=i, fontsize=heights[i]*0.5+3, color=color)
                
mybars(heights, "blue", "k-fold")
mybars(shuffle, "red", "Phenotype Shuffle")

plt.legend(loc="upper left")

# Adding labels and title
plt.xlabel('Number of SNP')
plt.ylabel('Frequency')
plt.title('Histogram of SNPs')

plt.show()