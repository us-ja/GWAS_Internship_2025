
import subprocess
import sys
import random 
import numpy as np
from datetime import datetime
import os  
sys.path.append('..')
from my_utils import *
o = sys.stdout   #define std as o

def combine_build_up(group_size:int, k_pers:int=None, bounded:bool=True, shuffle:bool=True, recover:str=None, in_subdir:str=None, in_file:str=None,startlevel:int=0):
    '''combines  with given groupsize, if recover is a tuple specifiying dir, in_subdir, in_file then starts from matching files'''
    global ped_file, bim_file, total_snp 
    print("Started building at ", curr_time())
    level=startlevel
    if bounded:
        comment="seq_bound_enf"+str(group_size)+"_"
    else:
        comment="seq_split"+str(group_size)+"_"
    print("started build-up at", curr_time())
    method="given"
    level=0
    identified=list(range(total_snp))
    if shuffle:
        random.shuffle(identified)
    ends=[]
    for i in range(len(identified)//group_size+1):
        ends.append(i*group_size)
    
    while True:#or level< big number to prevent endless
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
                created_files.append(conversion(to_analyze, method,  comment, start, total=total_snp, dir=dir_l(level),))
            # print(created_files)
            
        else:
            created_files=get_files(recover, in_subdir, in_file)
            recover=None
        identified=set()
        
        ends=[0]
        for file_name in created_files:
            if file_name!=None:
                file = open(file_name)
                lines=file.readlines()
                for i in range(-4-int(lines[1]),-4):
                    ele= lines[i].split(sep=',')
                    ele[0] =ele[0][1:]
                    ele[-1]=ele[-1][:-2]
                    ele=list(map(int, map(float, ele)))
                    for j in range(len(ele)):
                        identified.add(ele[j])
                    if len(identified)-ends[-1]>=group_size:
                        ends.append(len(identified))  
                file.close()
        
        identified=list(identified)
        
        # print(identified, "identified")
        level+=1
        print("reached new level", level, curr_time())


    if len(identified)//group_size==0:#prevent entering this if levelled out and not finished
        f_res=(conversion(identified, method, comment,level, total=total_snp, k_pers=k_pers,))
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


total_snp=get_total_snp(fileprefix)# total_snp=170 #for tests only
# k_pers=60#for tests only
# combine_build_up(sys.argv[1])
print(curr_time())
print(conversion([161, 207, 362, 620, 786, 824, 867, 1178, 1209, 1219, 1231, 1334, 1806, 1854, 1917], "given", "worsetest", 8, fileprefix,delete_logs=False, allow_unknowns=10))
print(curr_time())
sys.stdout=o