import sys
sys.path.append('..')
import random
# from my_utils import *
a_pers=(random.sample(range(0,109), k= int(0.9*109)))
a_pers.sort()
b_pers=[]
i=0
j=0
while i<109:
    if (j>=len(a_pers) or i!=a_pers[j]):
        b_pers.append(i)
    else:
        j+=1
    i+=1
print(b_pers, "persons")
for seed in range(9,12):
# seed=11
    random.seed(seed)

    a_pers=(random.sample(range(0,109), k= int(0.9*109)))
    a_pers.sort()
    b_pers=[]
    i=0
    j=0
    while i<109:
        if (j>=len(a_pers) or i!=a_pers[j]):
            b_pers.append(i)
        else:
            j+=1
        i+=1
    print(b_pers, "persons")



