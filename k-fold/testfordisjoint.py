import sys
sys.path.append('..')
import random
# from my_utils import *
goods=[10]

forbidden=set([18, 29, 44, 49, 50, 68, 70, 98, 103, 105, 106])
b_pers=forbidden
seed=0
for i in range(5):
    while not b_pers.isdisjoint(forbidden):
        random.seed(seed)
        a_pers=(random.sample(range(0,109), k= int(0.9*109)))
        a_pers.sort()
        b_pers=set()
        i=0
        j=0
        while i<109:
            if (j>=len(a_pers) or i!=a_pers[j]):
                b_pers.add(i)
            else:
                j+=1
            i+=1
        seed+=1
    print(sorted(list(b_pers)))
    for e in b_pers:
        forbidden.add(e)
    goods.append(seed)
print(goods)

