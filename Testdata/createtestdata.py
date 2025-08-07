import sys
sys.path.append('..')
import random
from my_utils import *
res=[]

o=sys.stdout
total_snp=1000000
total_pers=109
seed=300
random.seed(300)
fileprefix="testdata"
ped=open(fileprefix+".ped", 'w')

sys.stdout=ped
snp_p= []
for i in range(total_snp):
    snp_p.append(random.uniform(0.05,0.5))
def get_total_pers(x=None, y=None):
    return total_pers
def get_total_snp(x=None, y=None):
    return total_snp
l=[]
for i in range(total_pers):
    line=[]
    for j in range(2):
        line.append(str(i))
    for j in range(4):
        line.append(str(1))
    for j in range(total_snp):
        if random.uniform(0,1)<snp_p[j]:
            a="A"
        else:
            a="G"
        if random.uniform(0,1)<snp_p[j]:
            b="A"
        else:
            b="G"
        
        
        line.append(a+" "+b)
        
    print('\t'.join(line))

ped.close()
fileprefix="testdata"
bim=open(fileprefix+".bim", 'w')
sys.stdout=bim
for i in range(len(snp_p)):
    line=[]
    for j in range(3):
        line.append(str(i))
    line.append(str(int(snp_p[i]*1000)))
    line.append("A")
    line.append("G")
   
        
        
        
        
    print('\t'.join(line))
    
bim.close()


sys.stdout=o