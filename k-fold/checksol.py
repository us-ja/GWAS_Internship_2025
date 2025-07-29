import sys
sys.path.append('..')
import random
from my_utils import *
seed=10
# compare("given9foldbound_enf200_4/result55.txt", ) 
# compare("given9fold_s2bound_enf200_4/result53.txt", )  
# compare("given9fold_s3bound_enf200_4/result54.txt", )  
# compare("given9fold_s96bound_enf200_4/result53.txt", )  
# compare("given9fold_s286bound_enf200_4/result52.txt", )         
               
        
print("Started at", curr_time())  

res=[]


dir="Res/"
for (root,dirs,files) in os.walk(dir):
    

        for e in files: 
            if ".DS" not in e:
                res.append(root+"/"+e)
for e in res:
    if "shuffle" not in e:
        print("\n Analysis of ",e)
        compare(e)
    
print("finished all at", curr_time())       
    
 
