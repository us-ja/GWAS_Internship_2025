import sys
sys.path.append('..')
from my_utils import *
import matplotlib.pyplot as plt
import numpy as np
import os

# Generate random data for the histogram


data=[]
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
        data.extend(ele)
    file.close()
print(data)
n=get_total_snp("../HapMap")
# Plotting a basic histogram
counts, bins, patches=plt.hist(data, bins=range(0, n, 1), color='skyblue', edgecolor='black')
plt.ticklabel_format(useOffset=False, style='plain')
for count, bin in zip(counts, bins):
    if count > 2:
        plt.text(bin, count, int(bin))
# Adding labels and title
plt.xlabel('Number of SNP')
plt.ylabel('Frequency')
plt.title('Histogram of SNPs')

# Display the plot
plt.show()