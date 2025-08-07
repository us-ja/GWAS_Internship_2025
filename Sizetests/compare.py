import sys
sys.path.append('..')
import random
import matplotlib.pyplot as plt
from my_utils import *
seed=10


print("Started at", curr_time())              

sh, seeds=get_shares(get_files(".", "given", "res", ),accept_lim=True, )

# print(sh, len(sh))
# print(seeds, len(seeds))

plt.figure(figsize=(10,5))
plt.title('Out of sample prediction accuracy')


# labels=["Sizetests\n"+str(len(sh)), "Ordered 25\n"+str(len(bound)), "Alternate\n"+str(len(alt_b)),"Pyramid shuffle \n"+str(len(kfold_s)),"Pyramid bound\n"+str(len(kfold_b))] 
plt.scatter(seeds, sh, label="Out of sample")
out, so=get_shares(get_files(".", "given", "res", ))
print(out,seeds)
plt.scatter(seeds,out, label="Not in last level")
# plt.violinplot([sh, bound, alt_b,kfold_s,kfold_b ],showmeans=False, showmedians=True , )
plt.ylabel('Share of correct predictions in %')
plt.xlabel('Method, Amt of predictions')

plt.legend()

plt.axhline(55/1.09, color='red', linestyle=':')
plt.subplots_adjust(left=None, bottom=0.14, wspace=None)
# plt.savefig('../Documentation/sizetest.eps', format='eps')
print("finished all at", curr_time())
plt.show()

 
