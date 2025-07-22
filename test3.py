
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
    print(list)
    new_list=[]
    for e in list:
        new_list.append(e[0])
        new_list.append(e[1])
    
    for i in range(len(new_list)):
        print("m=",i)
        if new_list[i]=='1':
            for k in range(len(d)):
                d[k]=d[k]+(2**(m-i-1))
        elif new_list[i]!='0':#then it's something else most probably unknown -
            print(new_list[i])
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
        print("ped")
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
    c2=0
    print('here 4')
    for e in idict:
        print(e)
            
    
    print("finsihed true")
    return True
    # print("selected risk allele's are:")
    # print(risk)
    lo.close()
        
    # with open(json_out, 'w') as f: 
    #     sys.stdout = f    
    #     print(idict)
    sys.stdout=o 
    n= len(selection)
    

    
method='sequential'
start=6
ending=".py"
transformation= "convert3"
hapmap= open("HapMap.ped")
lines= hapmap.readlines()
total_snp=len(lines[0].split('\t'))-6
n=200 #group size
comment="test3only_onlyconv"

value=start



to_combine=[]
def dir_l():
    return ""
# echo "Started with seed" $method$comment$value "at" $(date '+%B %V %T:')
print("tat")
mkdir(dir_l()+str(method)+str(comment)+str(start))
print(conversion(n, method, start, comment, total=total_snp, dir=dir_l()))
print( "Completed",start, "at", curr_time() )
    




print("Finished ",method,comment,value, " at ", curr_time())



# hapmap.close()


