
import subprocess
import sys
import random 
import numpy as np
from datetime import datetime
import os  
o = sys.stdout   #define std as o
def chromosomes_start():
    '''returns a list of all the start of the chromosomes'''
    global bim_file
    bim=open(bim_file)
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
def mkdir(name, option="-p"):  
    subprocess.run(str("mkdir "+option+" "+str(name)), shell=True)
def rm(name, option=""):
    subprocess.run(str("rm "+option+" "+name), shell=True)
def to_espresso(selection, lines, k_pers, risk, norisk):  
    idict = {}
    excluded_pers=0
    binary=("00", "01", "11", "10", "--")
    for line in lines:
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
                        assert len(risk)>=i, "snp_overflow" 
                        if risk[i]==e :
                            allele+=1  
                        elif norisk[i]!=e and "-" not in e:
                            print("major problem", risk[i], norisk[i], e, count, )
                            print(selection[i],i) 
                idict[indivual[1]]["snps"].append(binary[allele])   
                snp_num+=1        
        count+=1  
    doubles=0
    found=set()
    allow_unknowns=1
    print(".i ", (len(selection))*2)
    print(".o ", 1)
    print(".type fr")
    for e in idict:
        unknowns=count_unknown(idict[e]["snps"])
        
        if unknowns<allow_unknowns:
            
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
    # with open(json_out, 'w') as f: 
    #     sys.stdout = f    
    #     print(idict)
    return doubles, excluded_pers
def espresso_analysis(espresso_out, path, selection, doubles, excluded_pers, selection_type, seed, risk, norisk):
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
            if doubles==0 and doubles!=None:
                print(doubles, "duplicates were found, first seen is selected, increase amount of selceted SNPs and ", excluded_pers, "seq were exluded as too many don't cares")   
            else:
                print("no overspecification", excluded_pers, "seq were exluded as too many don't cares")   
            print(counter)
    return res_out
def espresso(input, output):
    subprocess.run(str("../../espresso-logic-master/bin/espresso "+input+" > "+output ), shell=True)
def conversion(select_snp, selection_type:str, comment:str, value:int, total:int=None, k_pers:int=None, dir:str="", delete_logs:bool=True):
    ''' '''
    global ped_file, bim_file
    mkdir(dir+str(selection_type)+str(comment)+str(value))
    out_before=sys.stdout
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

    if selection_type=="random" or selection_type=="seeded":
        random.seed(seed)
        selection=random.sample(range(6, total+6),k=amt_select_snp)
    elif selection_type=="given":
        selection=list(map(lambda x: x + 6, (map(abs, selection))))
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
        norisk.append(b_lines[e-6].split()[-1])
        risk.append(b_lines[e-6].split()[-2])
    bim.close()
    esp_in = open(txt_out, 'w') 
    sys.stdout=esp_in
    doubles, excluded_pers= to_espresso(selection,ped_lines,k_pers, risk, norisk)
    
    ped_file.close()

      
    espresso(txt_out, espresso_out)  
    
    
    res_out=espresso_analysis(espresso_out, path, selection, doubles, excluded_pers, selection_type, seed, risk, norisk)
    if delete_logs:
        rm(txt_out)
        rm(espresso_out)
    sys.stdout=out_before
    return res_out#make only if needed
def dir_l(level):
    return "l_"+str(level)+"/"
def get_files(dir, in_subdir=None, in_file=None):
    '''returns list of files in given dir with in_subdir/in_file specifing what must be part of path/filename'''
    created_files=[]
    for (root,dirs,files) in os.walk(dir):
        if in_subdir==None or "givenboundaries_enf200_" in root:

            for e in files:
                if in_file in e:
                    created_files.append(root+"/"+e)
    return(created_files)
def get_total_snp():
    global ped_file
    hapmap= open(ped_file)
    lines= hapmap.readlines()
    hapmap.close()
    return len(lines[0].split('\t'))-6
def combine_build_up(n:int, k_pers=None, bounded:bool=True, shuffle:bool=True, recover:str=None, in_subdir:str=None, in_file:str=None,startlevel:int=0):
    '''combines  with given groupsize, if recover is a tuple specifiying dir, in_subdir, in_file then starts from matching files'''
    global ped_file, bim_file, total_snp 
    print("Started building at ", curr_time())
    level=startlevel
    if bounded:
        comment="seq_bound_enf"+str(n)+"_"
    else:
        comment="seq_split"+str(n)+"_"
    print("started build-up at", curr_time())
    method="given"
    level=0
    identified=list(range(total_snp))
    if shuffle:
        random.shuffle(identified)
    ends=[]
    for i in range(len(identified)//n+1):
        ends.append(i*n)
    
    while True:#or level< big number to prevent endless
        if len(identified)//n==0:
            break
        if recover==None:
            created_files=[]
            if not bounded:
                ends=[]
                for i in range((len(identified)//n)+1):
                    ends.append(i*n)
            ends[-1]=len(identified)     #make last group bigger by combining the rest
            for i in range(len(ends)-1):
                
                start=ends[i]
                end=ends[i+1]
                to_analyze= identified[start:end]
                # print(to_analyze)
                created_files.append(conversion(to_analyze, method,  comment, start, total=total_snp, dir=dir_l(level),))
            # print(created_files)
            identified=set()
        else:
            created_files=get_files(recover, in_subdir, in_file)
            recover=None

        assert len(identified)==0, "identified not empty"
        ends=[0]
        for file_name in created_files:
            file = open(file_name)
            lines=file.readlines()
            for i in range(-4-int(lines[1]),-4):
                ele= lines[i].split(sep=',')
                ele[0] =ele[0][1:]
                ele[-1]=ele[-1][:-2]
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


    if len(identified)//n==0:#prevent entering this if levelled out and not finished
        f_res=(conversion(identified, method, comment,level, total=total_snp, k_pers=k_pers))
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

fileprefix="HapMap"
pedsuffix=".ped"
bimsuffix=".bim"
ped_file=fileprefix+pedsuffix
bim_file=fileprefix+bimsuffix
total_snp=get_total_snp()# total_snp=170 #for tests only
# k_pers=60#for tests only
# combine_build_up(sys.argv[1])
conversion(1000, "seeded", "test", 8)

sys.stdout=o