import sys
sys.path.append('..')
import random
from my_utils import *
import matplotlib.pyplot as plt
# predic_acc=conversion(6, "total", "total", 0, "testdata_2", delete_logs=False)     #does not work
# print(predic_acc)
# predic_acc=conversion(list(range(20)), "given", "total", 0, "testdata_2", delete_logs=False)#works
# print(predic_acc)
results=[]
start=10
end=300
steps=1
for i in range(start, end, steps):

    results.append(True)
    if i>1:
        fileprefix="testdata_1001"
        print("analysis of ", i)
        try:
            file=open("sequentialtotal6/result"+str(i)+".txt")
        except:
            file=open(conversion(i, "sequential", "total", 6, fileprefix, delete_logs=False))
            
        lines=file.readlines()
        file.close()
        

        countadd=0
        if int(lines[1])==0:
            pass
        if "added lines:\n" == lines[-2]:#is already amended
            added_lin=int(lines[-1])
            
        else:
            added_lin=0
        for j in range(-4-int(lines[1])-added_lin,-4-added_lin):
            if lines[j]=="[]\n":#no usable result
                pass
            else:
                print(lines[j][:-1])
                if lines[j][0]!="[":
                    print("irregularity with  ", lines[j],"at", i)
                if lines[j][:-1]!="[-1.5]" and lines[j][:-1]!="[-2.5]":
                    results[-1]=False
                    


correct=[]

for k in range(len(results)):
    if results[k]:
        correct.append(k*steps)
        # print(k)
        # plt.vlines(x=i, ymin=0, ymax=1, colors='red')
bin_s=10
hist=list(map(lambda x: x+start, correct))
print(hist)
plt.hist(hist, bins=list(range(start, end+bin_s, bin_s*steps)))
plt.show()



