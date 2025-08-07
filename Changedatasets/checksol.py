import sys
sys.path.append('..')
import random
import matplotlib.pyplot as plt
from my_utils import *
seed=10



print("Started at", curr_time())              

sh,=get_shares(get_files(".", "s1", "res", ["bound"]),accept_lim=True, )[0]
print(sh)
bound=get_shares(get_files(".", "s1", "res", ["shuffle"]),accept_lim=True)[0]

alt_b=get_shares(get_files(".", "alter", "res",),accept_lim=True)[0]

# alt_s=get_shares(get_files(".", "alter", "res",["bound"]))

kfold_b= get_shares(get_files("../k-fold", "bound", "res",) )[0]
kfold_s= get_shares(get_files("../k-fold", "shuffle", "res",))[0]

plt.figure(figsize=(10,5))
plt.title('Out of sample prediction accuracy')
# print(sh)
# print( np.quantile(sh, np.array([0.00, 0.25, 0.50, 0.75, 1.00]),method='closest_observation'))
# print(np.quantile(bound, 0.75), np.mean(bound))
# print( np.quantile(bound, np.array([0.00, 0.25, 0.50, 0.75, 1.00])))
# print(np.quantile(bound, 0.25), np.mean(bound))
data=[sh, bound, alt_b,kfold_s,kfold_b ]
labels=["Shuffle 25\n"+str(len(sh)), "Ordered 25\n"+str(len(bound)), "Alternate\n"+str(len(alt_b)),"Pyramid shuffle \n"+str(len(kfold_s)),"Pyramid bound\n"+str(len(kfold_b))] 
plt.boxplot(data,tick_labels=labels, medianprops=dict(color='blue'))

# plt.violinplot([sh, bound, alt_b,kfold_s,kfold_b ],showmeans=False, showmedians=True , )
plt.ylabel('Share of correct predictions in %')
plt.xlabel('Method, Amt of predictions')
for i in range(len(data)):
    # print(np.mean(data[i]))
    plt.scatter(i + 1, np.mean(data[i]), color='green')


plt.axhline(55/1.09, color='red', linestyle=':')
plt.subplots_adjust(left=None, bottom=0.14, wspace=None)
# plt.savefig('../Documentation/accuracyplot.eps', format='eps')
print("finished all at", curr_time())
plt.show()

 
