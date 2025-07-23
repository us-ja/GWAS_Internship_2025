
import subprocess
# subprocess.run("source ../venv/bin/activate", shell=True)
import sys
import random 
import numpy as np
from datetime import datetime
import os
start=6
ending=".py"
hapmap= open("HapMap.ped")
lines= hapmap.readlines()
total_snp=len(lines[0].split('\t'))-6
# total_snp=700
n=int(sys.argv[1]) #group size adjust 
comment="boundaries_enf"+str(n)+"_"
level=0
to_combine=[]
seed=40
random.seed(seed)
def curr_time():
    return str(datetime.now().strftime("%H:%M:%S"))
print("Started at ", curr_time())
all_selections=[]
def count_unknown(list):
    count=0
    for e in list:
        if "--" == e: 
            count+=1
    return count

def calculate_decimal(list):
    "calculates decimal numbers "
    d=[0]
    newlist=[]

    for e in list:
        newlist.append(e[0])
        newlist.append(e[-1])
    m=len(newlist)
    for i in range(m):
        if newlist[i]=='1':
            for k in range(len(d)):
                d[k]=d[k]+(2**(m-i-1))
        elif newlist[i]!='0':#then it's something else most probably unknown -
            if newlist[i]=='-':
                for k in range(len(d)):
                    d.append(d[k]+(2**(m-i-1))) 
            else:
                print(newlist[i], "inconsistency found")
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
    excluded_pers=0
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
        amt_select_snp=len(selection)

    
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
                    # selection=set()
                    # while len(selection)<amt_select_snp:
                    #     selection.add(random.randint(6,total))
                elif selection_type=="preselected" or selection_type=="given":
                    
                    selection=list(map(lambda x: x + 6, (map(abs, selection))))
                    
                    
                else:#treats it as sequential
                    if seq_start+amt_select_snp>total:
                        amt_select_snp=total-seq_start
                        print("overflow cut", total)
                    selection=list(range(seq_start,seq_start+amt_select_snp))
                path=dir+selection_type+comment+str(value)+"/"
                output=path+"output_"+str(amt_select_snp)
                overspecification_possible=True    #false if enough SNP's are selected
                    # if amt_select_snp<200:
                    #     overspecification_possible=True
                
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
    doubles=0
    found=set()
    allow_unknowns=1
    sys.stdout=o

    
                
    
    with open(txt_out, 'w') as esp_in:
        sys.stdout = esp_in
        print(".i ", (amt_select_snp)*2)
        print(".o ", 1)
        print(".type fr")
        for e in idict:
            unknowns=count_unknown(idict[e]["snps"])
            
            if unknowns<allow_unknowns:
                sys.stdout=lo
                dec=calculate_decimal(idict[e]["snps"]) 
                sys.stdout=esp_in    
                new=set(dec)
                if  found.isdisjoint(new):
                    found= found | new
                    for f in idict[e]["snps"]:
                        print(f, end="")
                    # print(" ",1)
                    print(" ",int(idict[e]["phenotype"])-1)
                else: #ignores if this excact combination of SNP was already seen
                
                    for g in dec:
                        doubles+=1
            else:
                excluded_pers+=1
        print(".e")
    
    sys.stdout = lo
    
    if doubles!=0:
        print(doubles, "duplicates were found, first seen is selected, increase amount of selceted SNPs")   
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
    res_out= path+"result"+str(n)+".txt"
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
                            error.append(str("inconsistency at column "+ str(i)+" that is snp "+ str(selected_snp[snp])+ " with:"+ str(line[i])+ "!"))
                    
                
                
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
            print((len(selection)-doubles-excluded_pers)*2)
            print("amount of identified SNPs:") 
            print(counter)
    rm(txt_out)
    rm(espresso_out)
    rm(log_out)
    sys.stdout=o
    return res_out#make only if needed

def espresso(input, output):
    
    subprocess.run(str("../../espresso-logic-master/bin/espresso "+input+" > "+output ), shell=True)

    


def dir_l(level):
    return "l_"+str(level)+"/"
# echo "Started with seed" $method$comment$value "at" $(date '+%B %V %T:')


def combine_build_up(n, total_snp):
    print("started build-up at", curr_time())
    method="given"
    level=0
    identified=list(range(total_snp))
    
    ends=[]
    
    first=True
    
    while True:#or level< big number to prevent endless
        if len(identified)//n==0 and not first:
            
            mkdir(str(method)+str(comment)+str(level))
            f_res=(conversion(identified, method, level, comment, total=total_snp))
            print( "finished at level", level, curr_time())
            print("the selection gave :")
            identified=set()
            file=open(f_res)
            lines=file.readlines()
            for i in range(-4-int(lines[1]),-4):
                ele= lines[i].split(sep=',')
                ele[0], ele[-1]=ele[0][1:], ele[-1][:-2]
                ele=(list( map(float, ele)))
                for j in range(len(ele)):
                    print(ele[j], end=", ")
            file.close()
            print()
            return 
        
        created_files=[]
        
        if not first:
            ends[-1]=len(identified)     #make last group bigger by combining the rest
            for i in range(len(ends)-1):
                start=ends[i]
                end=ends[i+1]
                mkdir(dir_l(level)+str(method)+str(comment)+str(start))
                to_analyze= identified[start:end]
                # print(to_analyze)
                created_files.append(conversion(to_analyze, method, start, comment, total=total_snp, dir=dir_l(level)))
        else:
            for (root,dirs,files) in os.walk("../Selectcomb/l_0/"):
                if "givenboundaries_enf200_" in root:
       
                    for e in files:
                        if "result" in e:
                            created_files.append(root+"/"+e)
            first=False
            print(created_files)

        identified=set()
        assert len(identified)==0, "identified not empty"
        ends=[0]
        for file_name in created_files:
            file = open(file_name)
            lines=file.readlines()
            for i in range(-4-int(lines[1]),-4):
                ele= lines[i].split(sep=',')
                ele[0] =ele[0][1:]
                ele[-1]=ele[-1][:-2]
                if ele[0][0]=="[":
                    print(ele, file_name)
                ele=list(map(int, map(float, ele)))
                for j in range(len(ele)):
                    identified.add(ele[j])
                if len(identified)-ends[-1]>=n:
                    ends.append(len(identified))
            file.close()
        
        identified=list(identified)
        
        # print(identified, "identified")
        level+=1
        print("reached new level", level, curr_time())
combine_build_up(n, total_snp)