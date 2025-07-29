import sys
sys.path.append('..')
import random
from my_utils import *
seed=10
def only_not_in(x):
    return x>99

# print("all not in last level")
# compare("l_3/given50per_lbound_enf200_0/result203.txt", ) 
# compare("given50per_lbound_enf200_4/result7.txt","\n")  
# print("")
# print("only not part of data") 
# compare("l_3/given50per_lbound_enf200_0/result203.txt", accept=only_not_in) 
# compare("given50per_lbound_enf200_4/result7.txt", accept=only_not_in)         
   
print("Started at", curr_time())              
res=["Res/given25_s127bound_enf200_4/result22.txt"]
for i in range(100,130) :
    pass
for e in res:
    print("\n Analysis of ",e)
    compare(e)
    
print("finished all at", curr_time())
 
