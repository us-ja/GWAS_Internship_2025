import os

for (root,dirs,files) in os.walk("Selectcomb/l_0/"):
    if "givenshuffle_rand200_" in root:
       
        for e in files:
            if "result" in e:
                print(root+"/"+e)
    
    