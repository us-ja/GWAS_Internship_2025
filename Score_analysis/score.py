import os
import sys
import numpy
import random
import matplotlib.pyplot as plt
selections=[[579852.5, -462318, 49044.5, 650422.5, 555449, -810289, 660188.5, 254566.5, 358117.5],
            [-440736, -964734, 652329.5, -656695, -113367, 579852.5, 345358.5, -838861, 555449],
            [308225.5, 567913.5, 495729.5, -981291, 929552.5, 509722.5, -431841, 773926, -964734, -184344],
            [-113367, 8876.5, -1021108, -200016, 630544.5, 37042.5, 434836.5, 650265.5, 765307],
            [-363513, 652329.5, -908103, 579852.5, -113367, 708439.5, 765307, 555449],
            [431841, 652329, 555449, 579852, 630544, 113367, 650265, 964734]
]
selections=[[652329, -630544]]

assoc= open("Score_analysis/adjusted_assoc_results.assoc")
a_lines=assoc.readlines()

def score(selection, a_lines):
    result = 0
    for e in selection:
        sign=1
        if e != abs(e):
            sign=-1
        normalized=int(abs(e))
        var=a_lines[normalized+1].split()
        print(var)
        if var[-1]!='NA' and float(var[-1])!=0:
            result += numpy.log10((float(var[-1])))*sign
    return round(float(result),2)

def rand_sign(x):
    y=0
    while y==0:
        y=random.randint(-1,1)*x
    print(y)
    return y

assoc.close()
res_score=[]
randscore=[]
for e in selections:
    res_score.append(score(e, a_lines))
for e in selections:
    rand_size=len(e)
    for i in range(40):
        selection=list(map(rand_sign, random.sample(range(1, len(a_lines)),k=rand_size)))
        
        # print(selection)
        randscore.append(score(selection, a_lines))
# randscore=list(map(lambda x: round(x, 2), randscore))
print(res_score)
print(randscore)
plt.boxplot([res_score, randscore])
plt.show()



