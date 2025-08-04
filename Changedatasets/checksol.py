import sys
sys.path.append('..')
import random
import matplotlib.pyplot as plt
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
def get_shares(files):
    alt=[]
    files.sort()
    for e in files:
        print("\n Analysis of ",e)
        alt.append(compare(e))
        if alt[-1]==None:
            alt.pop()
    return alt
print("Started at", curr_time())              
res=get_files(".", "s1", "res", ["bound"])
sh=get_shares(res)

res=get_files(".", "s1", "res", ["shuffle"])
bound=get_shares(res)

res=get_files(".", "alter", "res",["shuffle"])
alt_b=get_shares(res)
res=get_files(".", "alter", "res",["bound"])
alt_s=get_shares(res)


    
plt.title('Selection Scheme: Out of sample prediction accuracy')
plt.boxplot([sh, bound, alt_s, alt_b], tick_labels=["Shuffle 25\n"+str(len(sh)), "Ordered 25\n"+str(len(bound)), "Shuffle half\n"+str(len(alt_s)), "Bound half\n"+str(len(alt_b))])
plt.ylabel('Share of correct predictions in %')
# plt.savefig('../Documentation/selbox.eps', format='eps')
plt.show()
print("finished all at", curr_time())
 
