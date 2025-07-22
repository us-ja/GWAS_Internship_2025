import sys
sys.path.append('..')
import random
from my_utils import *
seed=10


def compare(result, prefix:str="HapMap"):
    products=[]
    file=open(result)
    lines=file.readlines()
    for i in range(-4-int(lines[1]),-4):
        ele= lines[i].split(sep=',')
        ele[0] =ele[0][1:]
        ele[-1]=ele[-1][:-2]
        ele=list( map(float, ele))
        products.append(ele)
    file.close()

    
    
    b_pers=[]
    
    a_pers= lines[-8-int(lines[1])].split(',')
    a_pers[0], a_pers[-1]=a_pers[0][1:], a_pers[-1][:-2]
    a_pers=list(map(int, a_pers))
    
    print(a_pers, "stop")

    i=0
    j=0
    hap= open(prefix+".ped")
    lines=hap.readlines()
    hap.close()
    while i<len(lines):
        if i!=a_pers[j]:
            b_pers.append(i)
        else:
            j+=1
        i+=1
    print(b_pers, "check if correct")
    
    for e in b_pers:
        print(diagnose_pers(products,e, prefix))


def diagnose_pers(products:list, e:str, prefix:str="HapMap", lines=None):
    '''edge case where -0 is identified as 0, binary=("00", "01", "11", "10", "--")'''
    if lines==None:
        hap= open(prefix+".ped")
        lines=hap.readlines()
        hap.close()
    indivual=(lines[e]).split('\t')
    maxshare=0
    phenotype=int(indivual[5])-1
    for p in products:
        state=True
        falses=0
        for snp_num in p:
            if snp_num==int(snp_num):
                first=True
            else:
                first=False
            if snp_num==abs(snp_num):
                pos=True
            else:
                pos=False
            snp=(indivual[int(abs(snp_num))+6][0], indivual[int(abs(snp_num))+6][-1])
            a, b= select_risk_al(prefix+".bim", [int(abs(snp_num))+6])
            risk, norisk= a[0], b[0]
            allele=0
            for e in snp :
                if e=="0":
                    allele=4
                else: 
                    if risk==e :
                        allele+=1  
                    elif norisk!=e and "-" not in e:
                        print("major problem", risk, norisk, e)
            
      
            if pos:
                if allele==0:
                    falses+=1
                elif allele==1 and first:                    
                    falses+=1
            else:
                if allele==2:                    
                    falses+=1
                elif allele==1 and not first:                    
                    falses+=1
            # print(allele, a, snp, snp_num, pos, first, falses)
        if falses==0:
        
                
            return True, phenotype
        share= (len(p)-falses)/len(p)
        if share>maxshare:
            maxshare=share
    return maxshare, phenotype


            

compare("exampleresult.txt")         
               
        
         
    
 
