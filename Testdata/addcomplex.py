import sys
sys.path.append('..')
import random
from my_utils import *
res=[]
fileprefix="testdata"

choosen=3+6

hap=open(fileprefix+".ped")
l=hap.readlines()
hap.close()

def sel_fun(l, prod, lit, seed, min_need, max_need):
    print(prod, lit, seed, min_need, max_need)
    total_snp=len(l[0].split('\t'))-6
    count=0
    pers=len(l)
    assert lit>0, "0 lit "
    if prod==1:
        while count<min_need or count>max_need:
            if pers-count>min_need and pers-count<max_need:
                print(liter)
                liter=list(map(lambda x: -x, liter))
                return liter, pers-count
            count=0
            liter=[]
            before=pers
            for i in range(lit):
                max_lost=pers- (i+1)*(pers-min_need)//lit
                min_loss=pers- (i+1)*(pers-max_need)//lit
                # print(max_lost, min_loss)
                while True:
                    liter.append(random.choice(range(-2*total_snp, 2*total_snp))/2)
                    count=0
                    for j in range(len(l)):
                        count+=diagnose_pers(liter, j, l)
                    # print(liter[0], count)
                    if count>max_lost and count<min_loss:
                        before=count
                        break
                    dev=before-count
                    if dev> max_lost and dev < min_loss:
                        liter[-1]=-liter[-1]
                        before=dev
                        break
                    liter.pop()
        return liter, count
            
    print("here")
    
    func, pers = sel_fun(l, prod-1, lit, min_need=min_need-min_need//prod, max_need=max_need-max_need//prod)
    f2, pers2=(sel_fun(l, 1, lit, min_need=min_need-pers, max_need=max_need-pers))
    return func, pers+pers2

def sel_ids(function, l):
    ids=[]
    for i in range(len(l)):
        diagnose=False
        if diagnose_pers(function, i, l):
            var=l[i].split('\t')
            ids.append(var[1])
    return ids





def diagnose_pers(liter:list, indiv:int, lines=None):
    '''edge case where -0 is identified as 0, binary=("00", "01", "11", "10", "--")'''
    indivual=(lines[indiv]).split('\t')
    assert len(liter)>0, "no literals given"
    for snp_num in liter:
        if snp_num==int(snp_num):
            first=True
        else:
            first=False
        if snp_num==abs(snp_num):
            pos=True
        else:
            pos=False
        snp=(indivual[int(abs(snp_num))+6]).split()
        risk, norisk= "A", "G"
        allele=0
        for e in snp :
            if e=="0":
                allele=4
            else: 
                if risk==e :
                    allele+=1  
                elif norisk!=e and "-" not in e:
                    print("major problem", risk, norisk, e)
                    countadd+=1
    
        if pos:
            if allele==0:
                return 0
            elif allele==1 and first:                    
                return 0
        else:
            if allele==2:                    
                return 0
            elif allele==1 and not first:                    
                return 0
    return 1
        
        


for seed in range(1,10):
    print("seed",seed)
    random.seed(seed)
    fun, pers=sel_fun(l,2,seed, seed, min_need=45, max_need=60)
    ids=sel_ids(fun, l)
    print(fun, len(ids))
    # grouping(fileprefix, seed, 200, plines=l, change_pheno=(lambda x: 1 if x in ids else 0), total_snp=1000)