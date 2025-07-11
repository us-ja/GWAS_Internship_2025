
import subprocess
# subprocess.run("source ../venv/bin/activate", shell=True)
import sys
import random 
import numpy as np
from datetime import datetime
import os

def curr_time():
    return str(datetime.now().strftime("%H:%M:%S"))

all_selections=[]
def calculate_decimal(list):
    "calculates decimal number treatings all - as 0"
    d=[0]
    m=len(list)
    for i in range(m):
        if list[i]==1:
            for k in range(len(d)):
                d[k]=d[k]+(2**(m-i-1))
        elif list[i]!=0:#then it's something else most probably unknown -
            for k in range(len(d)):
                d.append(d[k]+(2**(m-i-1))) 
    return d
def mkdir(name):  
    subprocess.run(str("mkdir -p "+str(name)), shell=True)
def rm(name, option=""):
    subprocess.run(str("rm "+option+" "+name), shell=True)
# subprocess.Popen("cd Selectcomb/", shell=True)
# subprocess.run("source ../venv/bin/activate", shell=True)
def conversion(select_snp, selection_type, value, comment, ped_file='HapMap.ped', total=None, k_pers=None, dir=""):
    #k_pers number of persons considered, select the first n persons, or higher, 
     #if total is not selected
     #if not specified selects first k snp's, possilble selection modes: random, seeded, total, sequential, preselected
    if selection_type=="preselected":
        selection=[]
        preselected = open(str(select_snp))
        selected = preselected.readlines()
        amt_select_snp=len(selected)
        for e in selected:
            selection.append(int(e[:-1])+6)

        preselected.close()
    elif selection_type=="given":
        #select_snp is a list
        selection=select_snp 
    
    else:
        amt_select_snp=int(select_snp)
       
    if selection_type=="preselected" or selection_type=="given":
        seed=0
        seq_start=6
    if selection_type=='seeded' :
        seed=int(sys.argv[3])
        seq_start=6
    else:
        seq_start=int(value)
        seed=None
   
    binary=("00", "01", "11", "10", "--")
    o = sys.stdout   #define std as o
    #make dictionary for all allele for each SNP
    
    # if amt_select_snp<200:
    #     overspecification_possible=True
        
    with open(ped_file) as file:
        
        lines = file.readlines()
        count=0 #counts the lines
        idict = {}
        inc_col=set()
        risk=[None]*(amt_select_snp)
        for line in lines:
            if count==0:
                if total==None:
                    total=len(line.split('\t'))-6
                if selection_type=="total":
                    amt_select_snp=total
                if total<amt_select_snp:
                    amt_select_snp=total
                if selection_type=="random":
                    seed=random.randint(0,amt_select_snp)
                

                if selection_type=="random" or selection_type=="seeded":
                    random.seed(seed)
                    selection=random.sample(range(6, total+6),k=amt_select_snp)
                    selection.sort()
                    # selection=set()
                    # while len(selection)<amt_select_snp:
                    #     selection.add(random.randint(6,total))
                elif selection_type=="preselected" or selection_type=="given":
                    selection.sort()
                    pass
                else:#treats it as sequential
                    if seq_start+amt_select_snp>total:
                        amt_select_snp=total-seq_start
                        print("overflow cut", total)
                    selection=list(range(seq_start,seq_start+amt_select_snp))
                path=dir+selection_type+comment+str(value)+"/"
                output=path+"output_"+str(amt_select_snp)
                overspecification_possible=False    #false if enough SNP's are selected
                
                log_out= output+".log"
                txt_out= output+".txt"
                json_out=output+".json"
                lo= open(log_out, 'w')
                sys.stdout=lo
                
                print("persons:=",k_pers)
                print("seed=",seed) 
                print("amt_select_snp=",amt_select_snp) #important that prints amount of SNP's
                print("input=", input)
                print("output=", output)
                print("selection_type=", selection_type) #if not specified selects first k snp's, possilble selection modes: random, seeded, total, sequential
                print("seq_start=", seq_start)
                print("overspecification_possible=", overspecification_possible)
                print("Selection was done using", selection_type, "as method with seed", seed, ", following selection was made:")
                print(selection)
                print("The ", 1,". is taken as reference, so 1 means same as the",1,". person while 0 means the other possibilities for each SNP consider the bim-file for further investigation.")
                
            if k_pers==None or count<k_pers:#always true if all person's are considered
                indivual=line.split('\t')
                idict[indivual[1]] = {"snps": [], "phenotype": indivual[5]}
                snp_num=0
                
                # assert len(selection)==amt_select_snp, "error while selecting amount of selected elements does not match the instructed amount"
                for i in selection: 
                    allele=0
                    snp=(indivual[i][0], indivual[i][-1])
                    
                    for e in snp :
                        if e=="0":
                            allele=4
                            break
                        else: 
                            assert len(risk)>=snp_num, "snp_overflow"
                            if risk[snp_num]==None:
                                risk[snp_num]=e  
                            if risk[snp_num]==e :
                                allele+=1  
                    idict[indivual[1]]["snps"].append(binary[allele])   
                    snp_num+=1        
            count+=1  
    doubles=[]
    found=set()
    with open(txt_out, 'w') as g:
        sys.stdout = g
        print(".i ", amt_select_snp*2)
        print(".o ", 1)
        print(".type fr")
        print(".p", len(idict))
        for e in idict:
            if overspecification_possible==True:
                dec=calculate_decimal(idict[e]["snps"])     
                new=set(dec)
                if  found.isdisjoint(new):
                    found= found | new
                    for f in idict[e]["snps"]:
                        print(f, end="")
                    # print(" ",1)
                    print(" ",int(idict[e]["phenotype"])-1)
                else: #ignores if this excact combination of SNP was already seen
                    
                    for g in dec:
                        doubles.append(dec)
            else:#overspecification is assumed to unprobable
                for f in idict[e]["snps"]:
                    print(f, end="")
                print(" ",int(idict[e]["phenotype"])-1)
        # print(".e")
    
    sys.stdout = lo
    if overspecification_possible==False:
        if len(doubles)!=0:
            print(len(doubles), "duplicates were found, first seen is selected and they were", doubles, "increase amount of selceted SNPs")   
        else:
            print("no overspecification")   
    print("k_pers=",count) 
    # print("selected risk allele's are:")
    # print(risk)
    lo.close()
        
    # with open(json_out, 'w') as f: 
    #     sys.stdout = f    
    #     print(idict)
    sys.stdout=o 
    n= len(selection)
    
    espresso_out=path+"analysis_"+str(n)+".txt"
    espresso(txt_out, espresso_out)  
    res_out= path+"/result"+str(n)+".txt"
    selected_snp=list(map(lambda x: x - 6, selection))
    second=0
    first=0
    stats=[]
    error=[]
    with open(res_out,'w') as outgoing:
        sys.stdout=outgoing
        with open(espresso_out) as e_file:    
            result=[]
            lines = e_file.readlines()
            for line in lines:
                if line[0]!="." and line[0]!="#":
                    result.append([])
                    for i in range(len(line)):
                        snp=i//2    #corresponding to pos k
                        if line[i]=="1":
                            if i%2==1:
                                second+=1
                                plus=0.5
                            else:
                                first+=1
                                plus=0
                            stats.append(snp)
                            result[-1].append(selected_snp[snp]+plus)
                        elif line[i]=="0":
                            if i%2==1:
                                second+=1
                                plus=0.5
                            else:
                                first+=1
                                plus=0
                            stats.append(snp)
                            result[-1].append(-selected_snp[snp]-plus)
                        elif line[i]=="-":
                            pass
                        elif line[i]==" " or line[i]==" ":
                            break
                        else:
                            error.append("inconsistency at column", i,"that is snp", selected_snp[snp], "with:", line[i], "!")
                    
                
                
                else:#ignore all lines generated by espresso or comments
                    pass
            counter=0
            print("products:")
            print(len(result))
            print("first:")
            print(first)
            print("second:")
            print(second)
            print("var:")
            print(np.var(stats)/len(selection))#apartness in regards of selection
            print("Selection:")
            print(selected_snp)#selection
            print(seed)
            print("Risk allele:")
            print(risk)
            print("error:", len(error))
            for e in error:
                print(e)
            print("result:")
            for e in result:
                counter+=len(e)
                print(e)
            print("input length (.i)")
            print(len(selection))
            print("amount of identified SNPs:") 
            print(counter)
    # rm(method+str(comment)+str(value)+"/analysis_"+str(n)+".txt")
    # rm(method+str(comment)+str(value)+"/output"+str(n)+".txt")
    # rm(method+str(comment)+str(value)+"/output"+str(n)+".log")
    sys.stdout=o
    return res_out#make only if needed
def espresso(input, output):
    
    subprocess.run(str("../../espresso-logic-master/bin/espresso "+input+" > "+output ), shell=True)

    
method='sequential'
start=6
ending=".py"
transformation= "convert3"
hapmap= open("HapMap.ped")
lines= hapmap.readlines()
total_snp=len(lines[0].split('\t'))-6
n=1700 #group size
comment="comparison"

value=start



to_combine=[]
def dir_l():
    return ""
# echo "Started with seed" $method$comment$value "at" $(date '+%B %V %T:')

mkdir(dir_l()+str(method)+str(comment)+str(start))
to_combine.append(conversion(n, method, start, comment, total=total_snp, dir=dir_l()))
print( "Completed",start, "at", curr_time() )
    




print("Finished ",method,comment,value, " at ", curr_time())



# hapmap.close()


