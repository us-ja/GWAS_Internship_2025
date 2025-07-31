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
def select_risk_al(bim_file, selection, b_lines=None):
    risk=[]
    norisk=[]
    if b_lines==None:
        bim=open(bim_file)
        b_lines=bim.readlines()
        bim.close()
    for e in selection:
        e_line=b_lines[e-6].split()
        norisk.append(e_line[-1])
        risk.append(e_line[-2])
    return risk, norisk
def print_line(idict, e, change_pheno):
    for f in idict[e]["snps"]:
        print(f, end="")
    # print(" ",1)
    if change_pheno==None:
        print(" ",int(idict[e]["phenotype"])-1)
    else:
        print(" ",change_pheno(e))
def to_espresso(selection:list, sel_pers:list, lines:list, risk:list, norisk:list,  esp_in:str, allow_unknowns=20, change_pheno=None, checkdoubles=True): 
    
    idict = {}
    o=sys.stdout
    
    excluded_pers=0
    binary=("00", "01", "11", "10", "--")
    for h in sel_pers:
        assert h>=0 and h<len(lines), "selected person is not in range"
        line=lines[h]
        indivual=line.split('\t')
        idict[indivual[1]] = {"snps": [], "phenotype": indivual[5]}
        snp_num=0
        
        # assert len(selection)==amt_select_snp, "error while selecting amount of selected elements does not match the instructed amount"
        for i in range(len(selection)): 
    
            allele=0
            snp=(indivual[selection[i]]).split()
            # snp=(indivual[selection[i]][0], indivual[selection[i]][2])
            
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
                        
                        print("major problem", risk[i], norisk[i], e)
                        print(selection[i],i) 
            idict[indivual[1]]["snps"].append(binary[allele])   
            snp_num+=1        
         
    doubles=0
    found=set()
    esp_out = open(esp_in, 'w')
    sys.stdout=esp_out
    print(".i ", (len(selection))*2)
    print(".o ", 1)
    print(".type fr")
    person=0
    for e in idict:
        unknowns=count_unknown(idict[e]["snps"]) 
        if allow_unknowns==None or unknowns<=allow_unknowns:
            if checkdoubles:
                dec=calculate_decimal(idict[e]["snps"]) 
                new=set(dec)
                if  found.isdisjoint(new):
                    found= found | new
                    print_line(idict, e, change_pheno)
                else: #ignores if this excact combination of SNP was already seen
                    sys.stdout=o
                    print("excluded ", e, "because", unknowns, "where detected")
                    print_line(idict, e, change_pheno)#add i and change e with person for easier access
                    sys.stdout=esp_out
                    doubles+=1
            else:
                print_line(idict, e, change_pheno)
        else:
            sys.stdout=o
            print("excluded ", e, "because", unknowns, "where detected")
            print_line(idict,e,change_pheno)
            sys.stdout=esp_out
            excluded_pers+=1
        person+=1
    print(".e")
    sys.stdout=o
    esp_out.close()
    # with open(json_out, 'w') as f: 
    #     sys.stdout = f    
    #     print(idict)
    return doubles, excluded_pers
def espresso_analysis(espresso_out, path, selection, doubles, excluded_pers, selection_type, seed, risk, norisk, sel_pers):
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
            print("seed:")
            print(seed)
            print("error:", len(error))
            for e in error:
                print(e)
            print("Risk allele:")
            print(risk)
            print("Normal (norisk) allele:")
            print(norisk)
            print("selection_type=", selection_type) #if not specified selects first k snp's, possilble selection modes: random, seeded, total, sequential
            print("result:")
            print("input length (.i)")
            print((len(selection))*2)
            print("Sel_pers:")
            print(sel_pers)
            print("number of excluded pers:")
            print(excluded_pers)
            if doubles!=0 and doubles!=None:
                print(doubles, "duplicates were found, first seen is selected, increase amount of selceted SNPs and ", excluded_pers, "seq were exluded as too many don't cares")   
            else:
                print("no overspecification", excluded_pers, "seq were exluded as too many don't cares")   
            counter=0
            for e in result:
                counter+=len(e)
                print(e)
            print("Products:")
            print(len(result))
            print("Literals/ num of SNP:")
            print(counter)
    return res_out
def espresso(input, output):
    '''runs espresso with input and ouput to output'''
    subprocess.run(str("../../espresso-logic-master/bin/espresso "+input+" > "+output ), shell=True)
def conversion(select_snp, selection_type:str, comment:str, value:int, fileprefix:str='HapMap',total:int=None, dir:str="", delete_logs:bool=True, allow_unknowns:str=20, stopifoverspecif:bool=False, sel_pers:list=[], change_pheno=None, checkdoubles=True, seed=None):
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
    ped.close()
    if sel_pers==[]:
        sel_pers=list(range(0,len(ped_lines)))
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
        if seed==None:
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
    risk, norisk = select_risk_al(bim_file, selection)

    
    
    
    doubles, excluded_pers= to_espresso(selection,sel_pers, ped_lines, risk, norisk,txt_out,allow_unknowns, change_pheno=change_pheno, checkdoubles=checkdoubles)
    
    
    if stopifoverspecif and doubles!=0:
        if delete_logs:
            rm(txt_out)
        return None 

      
    espresso(txt_out, espresso_out)  
    
    
    res_out=espresso_analysis(espresso_out, path, selection, doubles, excluded_pers, selection_type, seed, risk, norisk, sel_pers)
    if delete_logs:
        rm(txt_out)
        rm(espresso_out)
    sys.stdout=out_before
    
    return res_out#make only if needed
def dir_l(level:int):
    return "l_"+str(level)+"/"
def notcontain(forbidden:list, s:str):
    for e in forbidden:
        if e in s:
            return False
    return True
def get_files(dir:str, in_subdir:str=None, in_file:str=None, not_in_subdir:list=None, not_in_file:list=None):
    '''returns list of all files in given dir with in_subdir/in_file specifing what must be part of path/filename doesn't omits files with point/hidden files'''
    created_files=[]
    for (root,dirs,files) in os.walk(dir):
        if (in_subdir==None or in_subdir in root) and (not_in_subdir==None or notcontain(not_in_subdir, root)) :

            for e in files:
                if (in_file ==None or in_file in e) and (not_in_file==None or notcontain(not_in_file, in_file)):
                    
                    created_files.append(root+"/"+e)
    return(created_files)
def get_total_snp(fileprefix:str):
    hapmap= open(fileprefix+".ped")
    lines= hapmap.readlines()
    hapmap.close()
    return len(lines[0].split('\t'))-6
def get_total_pers(fileprefix:str):
    hapmap= open(fileprefix+".ped")
    lines= hapmap.readlines()
    hapmap.close()
    return len(lines)
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
def merge_sort(A,l,r, comparision_func=lambda x,y : (x>y) ):
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
        else:
            print("no evaluatable because of NA or 0 in OR column")
    return round(float(result),2)
def rand_sign(x:float)->float:
    '''returns given float with random sign -/+'''
    y=0
    while y==0:
        y=random.randint(-1,1)*x
    return y

def combine_build_up(group_size:int, dataprefix, total_snp:int=None , bounded:bool=True, shuffle:bool=True, recover:str=None, in_subdir:str=None, in_file:str=None,startlevel:int=0, deletelog:bool=True, sel_pers=[], add_comm:str="",seed:int=None, change_pheno=None, allow_unknowns:int=20, change_pers_func=None, checkdoubles:bool=True, shuffle_in_level:bool=False):
    '''combines  with given groupsize, if recover is a tuple specifiying dir, in_subdir, in_file then starts from matching files'''
    print("Started building at ", curr_time())
    if shuffle_in_level:
        bounded=False     #bounded is adapted automatically as no structure to preserve
    random.seed(seed)
    if total_snp==None:
        total_snp=get_total_snp(dataprefix)
    level=startlevel
    if bounded:
        comment=add_comm+"bound_enf"+str(group_size)+"_"
    elif shuffle_in_level:
        comment=add_comm+"shuffle"+str(group_size)+"_"
    else:
        comment=add_comm+"split"+str(group_size)+"_"
    
    method="given"
    level=0
    identified=list(range(total_snp))
    if shuffle:
        random.shuffle(identified)
    ends=[]
    for i in range(len(identified)//group_size+1):
        ends.append(i*group_size)
    if change_pers_func!=None:
        o_sel_pers=sel_pers
    while True:#or level< big number to prevent endless
        if change_pers_func!=None:
            sel_pers=change_pers_func(level, o_sel_pers)
            assert len(sel_pers)!=0, "change pers function does not return in a correct format"
        if len(identified)//group_size==0:
            break
        if recover==None:
            created_files=[]
            if not bounded:
                ends=[]
                for i in range((len(identified)//group_size)+1):
                    ends.append(i*group_size)
            ends[-1]=len(identified)     #make last group bigger by combining the rest
            for i in range(len(ends)-1):
                
                start=ends[i]
                end=ends[i+1]
                to_analyze= identified[start:end]
                # print(to_analyze)
                created_files.append(conversion(to_analyze, method,  comment, start, fileprefix=dataprefix ,total=total_snp, dir=dir_l(level),stopifoverspecif=True, sel_pers=sel_pers, delete_logs=deletelog, change_pheno=change_pheno, allow_unknowns=allow_unknowns, checkdoubles=checkdoubles, seed=seed))
            # print(created_files)
            
        else:
            created_files=get_files(recover, in_subdir, in_file)
            recover=None
       
        identified=[]
        ends=[0]
        for file_name in created_files:

            if file_name!=None:
                new_identified=set()
                file = open(file_name)
                lines=file.readlines()
                for i in range(-4-int(lines[1]),-4):
                    ele= lines[i].split(sep=',')
                    ele[0] =ele[0][1:]
                    ele[-1]=ele[-1][:-2]
                    ele=list(map(int, map(float, ele)))
                    for j in range(len(ele)):
                        new_identified.add(ele[j])
                identified.extend(new_identified)
                if len(identified)-ends[-1]>=group_size:
                    ends.append(len(identified))  
                file.close()
        if shuffle_in_level:
            random.shuffle(identified)
        
        new_identified=set()#empty to avoid space being used
        # print(identified, "identified")
        level+=1
        print("reached new level", level, curr_time())


    if len(identified)//group_size==0:#prevent entering this if levelled out and not finished
        f_res=(conversion(identified, method, comment,level, fileprefix=dataprefix, total=total_snp, stopifoverspecif=True, sel_pers=sel_pers, delete_logs=deletelog, change_pheno=change_pheno, allow_unknowns=allow_unknowns, checkdoubles=checkdoubles, seed=seed))
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
        return f_res 

def compare(result, prefix:str="HapMap", accept=lambda x: True, showall=False):
    products=[]
    file=open(result)
    lines=file.readlines()
    for i in range(-4-int(lines[1]),-4):
        ele= lines[i].split(sep=',')
        ele[0] =ele[0][1:]
        ele[-1]=ele[-1][:-2]
        ele=list( map(float, ele))
        products.append(ele)
    file.close()

    b_pers=[]
    
    a_pers= lines[-8-int(lines[1])].split(',')
    a_pers[0], a_pers[-1]=a_pers[0][1:], a_pers[-1][:-2]
    a_pers=list(sorted(map(int, a_pers)))
    
    

    i=0
    j=0
    hap= open(prefix+".ped")
    lines=hap.readlines()
    hap.close()
    while i<len(lines):
        if (j>=len(a_pers) or i!=a_pers[j]) and accept(i):
            b_pers.append(i)
        else:
            j+=1
        i+=1
    print(b_pers, "persons")
    correct_pred=0
    fpos=0
    fneg=0
    

    hap= open(prefix+".ped")
    lines=hap.readlines()
    hap.close()
    bim=open(prefix+".bim")
    b_lines=bim.readlines()
    bim.close()
    for e in b_pers:
        share, pheno= (diagnose_pers(products,e, prefix, lines=lines, bimlines=b_lines))
        if (int(share)==pheno):
            correct_pred+=1
            if showall:
                print(round(share,2), pheno)
        else:
            if int(share)==1:
                fpos+=1
                print("False positive for person", e)
            else:
                fneg+=1
                print("False negative for person", e,"with share of", round(share,2))
    print("correct were ", correct_pred, "out of ", len(b_pers), "that is ", round(correct_pred/len(b_pers),3)*100,"%", "with", fpos, "false positives and ", fneg, " false negatives")


def diagnose_pers(products:list, e:str, prefix:str="HapMap", lines=None, bimlines=None):
    '''edge case where -0 is identified as 0, binary=("00", "01", "11", "10", "--")'''
    if lines==None:
        hap= open(prefix+".ped")
        lines=hap.readlines()
        hap.close()
    indivual=(lines[e]).split('\t')
    maxshare=0
    phenotype=int(indivual[5])-1
    for p in products:
        state=True
        falses=0
        for snp_num in p:
            if snp_num==int(snp_num):
                first=True
            else:
                first=False
            if snp_num==abs(snp_num):
                pos=True
            else:
                pos=False
            snp=(indivual[int(abs(snp_num))+6][0]).split()
            if bimlines==None:
                a, b= select_risk_al(prefix+".bim", [int(abs(snp_num))+6])
            else:
                a, b= select_risk_al(prefix+".bim", [int(abs(snp_num))+6], b_lines=bimlines)
            risk, norisk= a[0], b[0]
            allele=0
            for e in snp :
                if e=="0":
                    allele=4
                else: 
                    if risk==e :
                        allele+=1  
                    elif norisk!=e and "-" not in e:
                        print("major problem", risk, norisk, e)
      
            if pos:
                if allele==0:
                    falses+=1
                elif allele==1 and first:                    
                    falses+=1
            else:
                if allele==2:                    
                    falses+=1
                elif allele==1 and not first:                    
                    falses+=1
            # print(allele, a, snp, snp_num, pos, first, falses)
        if falses==0:
        
                
            return 1, phenotype
        share= (len(p)-falses)/len(p)
        if share>maxshare:
            maxshare=share
    return maxshare, phenotype
