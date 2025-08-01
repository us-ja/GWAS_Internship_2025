import sys
sys.path.append('..')
from my_utils import *
import matplotlib.pyplot as plt
import numpy as np
import os
import math

# Generate random data for the histogram

n=get_total_snp("../HapMap")



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
        
        for f in res:
            heights[f]+=1
        file.close()
    return heights

# print(heights)


def mybars(color, label, dir:str=".", in_subdir:str=None, in_file:str=None, not_in_subdir:list=None, not_in_file:list=None,  bottom=None, print_f=False, pres_h=False):
    files=get_files(dir, in_subdir, in_file, not_in_subdir, not_in_file, print_f=print_f)
    heights=get_res(files)
    first=True
    
        
    for i in range(len(heights)):
        if heights[i]!=0:
            if bottom==None:
                ymin=0
            else:
                ymin=bottom[i]
            if first:
                plt.vlines(x=i, ymin=ymin, ymax=ymin+heights[i], colors=color, label=label+" ("+str(len(files))+")", )
                first=False
            else:
                plt.vlines(x=i, ymin=ymin, ymax=heights[i]+ymin, colors=color)
            if ymin+heights[i]>2:
                plt.text(x=i, y=heights[i]+0.1+ymin, s=i, fontsize=(heights[i]+ymin)*0.7+1, color=color)
    if pres_h:
        return heights
k_fold=mybars( "blue", "k-fold", "../k-fold", "given", "result", ["Old", "l_", "Shuffle_Pheno", "Showcase"], pres_h=True)
mybars("red", "Phenotype Shuffle", "../Shuffle_Pheno", "given", "result", not_in_subdir=["l_"], print_f=True)
mybars( "green", "Selection", "../Changedatasets", "given", "result", bottom=k_fold)
plt.ticklabel_format(useOffset=False, style='plain')
plt.legend(loc="upper left")

# Adding labels and title
plt.xlabel('Number of SNP')
plt.ylabel('Frequency')
plt.title('Histogram of SNPs')
# plt.savefig('../Documentation/histall.eps', format='eps')
plt.show()