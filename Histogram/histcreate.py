import sys
sys.path.append('..')
from my_utils import *
import matplotlib.pyplot as plt
import numpy as np
import os
import math

# Generate random data for the histogram

n=get_total_snp("../HapMap")

shuffle=[0]*n
pyramid=[0]*n
files=get_files("../k-fold", "given", "result", ["Old", "l_", "Shuffle_Pheno", "Showcase"])
print(files)
def get_res(files):
    heights=[0]*n
    for e in files:
        file=open(e)
        lines=file.readlines()
        res=set()
        for i in range(-4-int(lines[1]),-4):
            ele= lines[i].split(sep=',')
            ele[0] =ele[0][1:]
            ele[-1]=ele[-1][:-2]
            res.update( map(int, map(abs,map(float, ele))))
        print(res)
        for f in res:
            heights[f]+=1
        file.close()
    return heights
heights=get_res(files)
# print(heights)
files=get_files("../Shuffle_Pheno", "given", "result", not_in_subdir=["l_"])
print(files)
shuffle=get_res(files)

files=get_files("../Changedatasets", "given", "result", )
print(files)
pyramid=get_res(files)

def mybars(heights, color, label, bottom=None):
    first=True
    
        
    for i in range(len(heights)):
        if heights[i]!=0:
            if bottom==None:
                ymin=0
            else:
                ymin=bottom[i]
            if first:
                plt.vlines(x=i, ymin=ymin, ymax=ymin+heights[i], colors=color, label=label, )
                first=False
            else:
                plt.vlines(x=i, ymin=ymin, ymax=heights[i]+ymin, colors=color)
            if ymin+heights[i]>2:
                plt.text(x=i, y=heights[i]+0.1+ymin, s=i, fontsize=(heights[i]+ymin)*0.7+1, color=color)
                
mybars(heights, "blue", "k-fold")
mybars(shuffle, "red", "Phenotype Shuffle")
mybars(pyramid, "green", "Selection", heights)
plt.ticklabel_format(useOffset=False, style='plain')
plt.legend(loc="upper left")

# Adding labels and title
plt.xlabel('Number of SNP')
plt.ylabel('Frequency')
plt.title('Histogram of SNPs')
# plt.savefig('../Documentation/histall.eps', format='eps')
plt.show()