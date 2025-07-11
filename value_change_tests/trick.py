import sys
import random 

#variables to play with

n=None#number of persons considered, select the first n persons, or higher, 
amt_select_snp=int(sys.argv[1]) #if total is not selected
selection_type=str(sys.argv[2]) #if not specified selects first k snp's, possilble selection modes: random, seeded, total, sequential
value = int(sys.argv[3])
comment=str(sys.argv[4])
if selection_type=='seeded':
    seed=int(sys.argv[3])
    seq_start=6
else:
    seq_start=int(sys.argv[3])
    seed=None
path=selection_type+comment+str(value)+"/"
input='HapMap.ped'
output=path+"output_"+str(amt_select_snp)
overspecification_possible=False    #false if enough SNP's are selected
# if amt_select_snp<200:
#     overspecification_possible=True
log_out= output+".log"
txt_out= output+".txt"
json_out=output+".json"
binary=("00", "01", "11", "10", "--")



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



o = sys.stdout   #define std as o

#make dictionary for all allele for each SNP
with open(log_out, 'w') as lo:
    
    with open(input) as file:
        
        lines = file.readlines()
        count=0 #counts the lines
        idict = {}
        inc_col=set()
        risk=[None]*(amt_select_snp)
        
        for line in lines:
            if count==0:
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
                else:#treats it as sequential
                    if seq_start+amt_select_snp>total:
                        amt_select_snp=total-seq_start
                        print("overflow cut", total)
                    selection=range(seq_start,seq_start+amt_select_snp)
                
                sys.stdout=lo
                
                print("n=",n)
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
                
            if n==None or count<n:#always true if all person's are considered
                var=line.split('\t')
                idict[var[1]] = {"snps": [], "phenotype": var[5]}
                snp_num=0
                
                # assert len(selection)==amt_select_snp, "error while selecting amount of selected elements does not match the instructed amount"
                for i in selection: 
                    allele=0
                    snp=(var[i][0], var[i][-1])
                    
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
                    idict[var[1]]["snps"].append(binary[allele])   
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
    print("n=",count) 
    print("selected risk allele's are:")
    print(risk)
    
# with open(json_out, 'w') as f: 
#     sys.stdout = f    
#     print(idict)
sys.stdout=o   