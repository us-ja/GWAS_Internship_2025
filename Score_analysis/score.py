import os
import sys
import numpy
import random
import matplotlib.pyplot as plt
selections=[
    [-440736, -652329, -579852, -838861, -345358, -113367, -555449.5, -656695, -964734],
    [-8876, -200016, -630544, -37042, -1021108, -434836, -113367, -650265, -765307.5],
    [-358117, -254566, -579852, -462318, -810289, -49044, -650422, -555449.5, -660188]
            
]


assoc= open("Score_analysis/adjusted_assoc_results.assoc")
a_lines=assoc.readlines()
assoc.close()
def score(selection, a_lines):
    result = 0
    for e in selection:
        sign=1
        if e != abs(e):
            sign=-1
        normalized=int(abs(e))
        var=a_lines[normalized+1].split()
        
        if var[-1]!='NA' and float(var[-1])!=0:
            result += numpy.log10((float(var[-1])))*sign
    return round(float(result),2)
def score_pos(selection, a_lines):
    result = 0
    for e in selection:
        var=a_lines[int(abs(e))+1].split()
        if var[-1]!='NA' and float(var[-1])!=0:
            result += abs(numpy.log10((float(var[-1]))))
    return round(float(result),2)
def rand_sign(x):
    y=0
    while y==0:
        y=random.randint(-1,1)*x
    
    return y


res_score=[]
randscore=[]
for e in selections:
    res_score.append(score(e, a_lines))
for e in selections:
    rand_size=len(e)
    for i in range(40000):
        selection=list(map(rand_sign, random.sample(range(1, len(a_lines)-1),k=rand_size)))
        
        # print(selection)
        randscore.append(score_pos(selection, a_lines))
# randscore=list(map(lambda x: round(x, 2), randscore))
print(res_score)
# print(randscore)
plt.title('PRS of selected SNP')
plt.boxplot([res_score,randscore])

plt.show()
def print_summary(list):
    print( numpy.mean(list), numpy.var(list))
print_summary(randscore)



