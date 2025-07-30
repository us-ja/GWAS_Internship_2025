import sys
sys.path.append('..')
from my_utils import *
import matplotlib.pyplot as plt
import numpy as np
import os

# Generate random data for the histogram

n=get_total_snp("../HapMap")
heights=[0]*n

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


plt.bar(list(range(n)), heights)



# Display the plot
plt.show()