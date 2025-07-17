
import random
import numpy
def rand_sign(x):
    y=0
    while y==0:
        y=random.randint(-1,1)*x
    return y
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
assoc= open("Score_analysis/adjusted_assoc_results.assoc")
a_lines=assoc.readlines()
assoc.close()
randscore=[]
randpos=[]
rand_size=8#len(a_lines-1)
for i in range(500000):
    selection=list(map(rand_sign, random.sample(range(1, len(a_lines)-1),k=rand_size)))
    randscore.append(score(selection, a_lines))
    randpos.append(score_pos(selection, a_lines))
def print_summary(list):
    print( numpy.mean(list), numpy.var(list))
print_summary(randscore)
print_summary(randpos)

