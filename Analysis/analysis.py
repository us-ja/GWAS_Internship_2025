import matplotlib.pyplot as plt
import numpy as np
import os

# methods=["seeded6", "sequentialold6","seededtest30","sequentialchr87726" ]


directory="value_change_tests/Results"

for path, dirs, file in os.walk(directory):
    dirs = sorted(dirs)
    print(file)
    break
print(dirs)



methods=[]
excluded=[]
x_min=50
x_max=900
for e in dirs:
    if "old" in e:
        excluded.append(e)
    print(e, "here")

    if "old" not in e and "new" not in e:#e not in excluded and "seq" in e:
        methods.append(e)
    
    pass
# methods.append("seededtrick6")
# methods.append("sequentialchr87726")
# print(methods)
num_snps=[]
nec_snps=[]
products=[]
first_share=[]
variances=[]


for method in methods:
    num_snps.append([])
    nec_snps.append([])
    products.append([])
    first_share.append([])
    variances.append([])
    
    files = os.listdir(directory+"/"+method+"/")
    print(files,"files")
    for file_name in files:
        print(file_name)
        # print(path+method+"/"+file_name)
        if ".txt"!=file_name[-4:] or file_name[0:3]!="res":
            # print(path+method+"/"+file_name, "is not a correct formatted file")
            pass
        else:
            f = open(path+"/"+method+"/"+file_name)
            print(path+"/"+method+"/"+file_name, "here")
            lines= f.readlines()
            if len(lines)<8:
                print(path+method+"/"+file_name, "not enough lines")
                pass
            elif int(lines[3])!=0:
                if x_min<=int(lines[1]) and int(lines[1])<=x_max :#and int(lines[1])%5==0:
                    num_snps[-1].append(int(lines[1]))
                    nec_snps[-1].append(int(lines[-1]))
                    products[-1].append(int(lines[3]))
                    # print(lines[7], int(lines[3]))
                    if int(lines[5])+(int(lines[7])!=int(lines[-1])) and "old" not in method:
                        for i in range(-4-int(lines[3]),-4):
                            ele= lines[i].split(sep=',')
                            ele[0], ele[-1]=ele[0][1:], ele[-1][:-2]
                            first=0
                            second=0
                            for j in range(len(ele)):
                                # print(float(ele[j]), "not here")
                                if int(float(ele[j]))==float(ele[j]):
                                    first+=1
                                else:
                                    second+=1
                    else:
                        first=float(lines[5])
                        second=float(lines[7])
                    first_share[-1].append(float(first/(first+second)))
                    variances[-1].append(float(lines[9]))
            f.close()
    

# print(num_snps)
# print(nec_snps)
# print(products)
# print(first_share)
# print(variances)
hspace = 0.2


for show in ["normal"]:#"seq_rand", "old_new"
    plotter='o'
    
    fig, axs = plt.subplots(2, 2)
    fig.suptitle(show, fontsize=16)
    j=0
    for i in range(len(methods)):
            #give possiblity to not select certain types
        visible=True
        if show=="chromosome":
            if "seq" not in methods[i]:
                visible=False
                j-=1
            
        color='C'+str(j)
        if show=="old_new":
            color='blue'
            if "old" in methods[i]:
                color='red'
        elif show=="seq_rand":
            color='blue'
            if "seq" in methods[i]:
                color='red'
        else:
            if j>=len(methods)/5:
                plotter='x'
            if j>=2*len(methods)/5:
                plotter='^'
            if  j>=3*len(methods)/5:
                plotter='*'
            if j>=4*len(methods)/5:
                plotter='v'
        marker=4
        alpha=0.3
        if visible:
            axs[0,0].plot(num_snps[i], nec_snps[i], plotter,markersize=marker, alpha= alpha,label=(methods[i]),color=color )
            axs[0,1].plot(num_snps[i], products[i],plotter,markersize=marker, alpha= alpha,color=color)
            axs[1, 0].plot(num_snps[i], first_share[i], plotter,markersize=marker, alpha= alpha,color=color)
            axs[1, 1].plot(num_snps[i], variances[i], plotter,markersize=marker, alpha= alpha,color=color)
        j+=1
    axs[0, 0].set_title('Number of SNP identified')
    axs[0, 1].set_title('Products')
    axs[1, 0].set_title('Share of the first element')
    axs[1, 1].set_title('Variance')
    for i in range(2):
        for j in range(2):
            # axs[i,j].set_xlim(x_min, x_max)
            pass
    fig.legend(loc='outside upper right')

    for ax in axs.flat:
        ax.set(xlabel='SNPs')
    plt.subplots_adjust(left=0.1, bottom=None, right=0.9125, top=0.9, wspace=None, hspace=0.5)
    plt.title(show)
    plt.show()
