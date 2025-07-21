import subprocess
import sys
import random 
import numpy as np
from datetime import datetime
import os  

def chromosomes_start(file_prefix:str):
    '''returns a list of all the start of the chromosomes'''
    bim=open(file_prefix+".bim")
    lines=bim.readlines()
    last=0
    count=0
    lst=[]
    for line in lines:
        var=line.split()
        if last!=int(var[0]):
            last=int(var[0])
            lst.append(count)
            # print(last)
        count+=1
    return lst
def curr_time():
    return str(datetime.now().strftime("%H:%M:%S"))
def count_unknown(lst:list):
    count=0
    for e in lst:
        if "--" == e: 
            count+=1
    return count
def calculate_decimal(lst:list):
    "calculates decimal numbers "
    d=[0]
    newlist=[]

    for e in lst:
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
def mkdir(name:int, option:str="-p"):  
    subprocess.run(str("mkdir "+option+" "+str(name)), shell=True)
def rm(name:str, option:str=""):
    subprocess.run(str("rm "+option+" "+name), shell=True)
def to_espresso(selection:list, lines:list, k_pers:int, risk:list, norisk:list,  esp_out:str, allow_unknowns=None): 
    
    idict = {}
    o=sys.stdout
   
    
    count=0
    excluded_pers=0
    binary=("00", "01", "11", "10", "--")
    for line in lines:
        if k_pers==None or count<k_pers:#always true if all person's are considered
            indivual=line.split('\t')
            idict[indivual[1]] = {"snps": [], "phenotype": indivual[5]}
            snp_num=0
            
            # assert len(selection)==amt_select_snp, "error while selecting amount of selected elements does not match the instructed amount"
            for i in range(len(selection)): 
                f= selection[i]
                allele=0
                snp=(indivual[selection[i]][0], indivual[selection[i]][-1])
                
                for e in snp :
                    if e=="0":
                        allele=4
                        break
                    else: 
                        if not len(risk)>=i:
                            print(risk)
                            assert len(risk)>=i, "snp_overflow" 
                        if risk[i]==e :
                            allele+=1  
                        elif norisk[i]!=e and "-" not in e:
                            sys.stdout=o
                            print("major problem", risk[i], norisk[i], e)
                            print(selection[i],i) 
                idict[indivual[1]]["snps"].append(binary[allele])   
                snp_num+=1        
        count+=1  
    doubles=0
    found=set()
    sys.stdout=esp_out
    print(".i ", (len(selection))*2)
    print(".o ", 1)
    print(".type fr")
    for e in idict:
        unknowns=count_unknown(idict[e]["snps"])
        
        if allow_unknowns==None or unknowns<=allow_unknowns:
            
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
                    doubles+=1
            
        else:
            excluded_pers+=1
    print(".e")
    sys.stdout=o
    # with open(json_out, 'w') as f: 
    #     sys.stdout = f    
    #     print(idict)
    return doubles, excluded_pers
def espresso_analysis(espresso_out, path, selection, doubles, excluded_pers, selection_type, seed, risk, norisk):
    '''reads out from espresso and creates result file containing the summary'''
    n=len(selection)
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
            print("Normal (norisk) allele:")
            print(norisk)
            print("error:", len(error))
            for e in error:
                print(e)
            print("selection_type=", selection_type) #if not specified selects first k snp's, possilble selection modes: random, seeded, total, sequential
            if selection_type=="seeded" or selection_type=="random":
                print("seed=",seed) 
            print("result:")
            counter=0
            for e in result:
                counter+=len(e)
                print(e)
            print("input length (.i)")
            print((len(selection))*2)
            print("number of excluded pers:")
            if doubles!=0 and doubles!=None:
                print(doubles, "duplicates were found, first seen is selected, increase amount of selceted SNPs and ", excluded_pers, "seq were exluded as too many don't cares")   
            else:
                print("no overspecification", excluded_pers, "seq were exluded as too many don't cares")   
            print("Products:")
            print(len(result))
            print("Literals/ num of SNP:")
            print(counter)
    return res_out
def espresso(input, output):
    '''runs espresso with input and ouput to output'''
    subprocess.run(str("../../espresso-logic-master/bin/espresso "+input+" > "+output ), shell=True)
def conversion(select_snp, selection_type:str, comment:str, value:int, fileprefix:str='HapMap',total:int=None, k_pers:int=None, dir:str="", delete_logs:bool=True, allow_unknowns:str=None, stopifoverspecif:bool=False):
    '''returns file name of the result executed according to input, A1 is selected as risk allele'''
    out_before=sys.stdout
    ped_file=fileprefix+".ped"
    bim_file=fileprefix+".bim"
    mkdir(dir+str(selection_type)+str(comment)+str(value))
    
    if selection_type=="given":
        #select_snp is a list
        selection=select_snp 
        amt_select_snp=len(selection)
        seq_start=6
    else:
        amt_select_snp=int(select_snp)
        if selection_type=='seeded' :
            seq_start=6
        else:
            seq_start=int(value)
            seed=None

    ped= open(ped_file) 
    
    ped_lines = ped.readlines()
    count=0 #counts the lines
    line=ped_lines[0]
    if total==None:
        total=len(line.split('\t'))-6
    if selection_type=="total":
        amt_select_snp=total
    if total<amt_select_snp:
        amt_select_snp=total
    if selection_type=="random":
        seed=random.randint(0,amt_select_snp)
    else:
        seed=value

    if selection_type=="random" or selection_type=="seeded":
        random.seed(value)
        selection=random.sample(range(6, total+6),k=amt_select_snp)
    elif selection_type=="given":
        selection=list(map(lambda x: x + 6, map(int,(map(abs, selection)))))
    else:   #treats it as sequential
        if seq_start+amt_select_snp>total:
            amt_select_snp=total-seq_start
            print("overflow cut", total)
        selection=list(range(seq_start,seq_start+amt_select_snp))
    path=dir+selection_type+comment+str(value)+"/"
    output=path+"output_"+str(amt_select_snp)
    
    
    txt_out= output+".txt"
    json_out=output+".json"
    
    
    espresso_out=path+"analysis_"+str(len(selection))+".txt"
    risk=[]
    norisk=[]
    bim=open(bim_file)
    b_lines=bim.readlines()
    
    for e in selection:
        e_line=b_lines[e-6].split()
        norisk.append(e_line[-1])
        risk.append(e_line[-2])
    bim.close()
    
    esp_in = open(txt_out, 'w') 
    
    doubles, excluded_pers= to_espresso(selection,ped_lines,k_pers, risk, norisk,esp_in,allow_unknowns)
    esp_in.close()
    ped.close()
    if stopifoverspecif and doubles!=0:
        if delete_logs:
            rm(txt_out)
        return None 

      
    espresso(txt_out, espresso_out)  
    
    
    res_out=espresso_analysis(espresso_out, path, selection, doubles, excluded_pers, selection_type, seed, risk, norisk)
    if delete_logs:
        rm(txt_out)
        rm(espresso_out)
    sys.stdout=out_before
    
    return res_out#make only if needed
def dir_l(level:int):
    return "l_"+str(level)+"/"
def get_files(dir:str, in_subdir:str=None, in_file:str=None):
    '''returns list of files in given dir with in_subdir/in_file specifing what must be part of path/filename'''
    created_files=[]
    for (root,dirs,files) in os.walk(dir):
        if in_subdir==None or "givenboundaries_enf200_" in root:

            for e in files:
                if in_file in e:
                    created_files.append(root+"/"+e)
    return(created_files)
def get_total_snp(fileprefix:str):
    hapmap= open(fileprefix+".ped")
    lines= hapmap.readlines()
    hapmap.close()
    return len(lines[0].split('\t'))-6
def fun(x,y):
    return x[0]>=y[0]
def merge_nicer(A,B, compar):
    i=0
    j=0
    C=[]
    last=None
    
    while i < len(A) or j < len(B):
        if j==len(B) or (i<len(A) and compar(A[i],B[j])):#fun(A[i],B[i])):
            C.append(A[i])
            i=i+1
        else:
            C.append(B[j])
            j=j+1
    return C
def merge_sort(A,l,r, comparision_func:function=lambda x,y : (x>y) ):
    if r-l == 0:
        return []
    if r-l == 1:
        return [A[l]]
    m=(l+r)//2
    L=merge_sort(A,l,m, comparision_func)
    R=merge_sort(A,m,r, comparision_func)
    return merge_nicer(L,R, comparision_func)
def score(selection:list, a_lines:list, only_pos:bool=False):
    result = 0
    for e in selection:
        sign=1
        if e != abs(e):
            sign=-1
        normalized=int(abs(e))
        var=a_lines[normalized+1].split()
        
        if var[-1]!='NA' and float(var[-1])!=0:
            if only_pos:
                result+=abs(np.log10(float(var[-1])))
            else:
                result += np.log10((float(var[-1])))*sign
    return round(float(result),2)
def rand_sign(x:float)->float:
    y=0
    while y==0:
        y=random.randint(-1,1)*x
    return y