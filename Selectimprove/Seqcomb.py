
import subprocess
import sys
import random 
import numpy as np
from datetime import datetime
import os  
sys.path.append('..')
from my_utils import *
o = sys.stdout   #define std as o


fileprefix="HapMap"


total_snp=get_total_snp(fileprefix)# total_snp=170 #for tests only


print(curr_time())
print(conversion([-440736, -652329, -579852, -838861, -345358, -113367, -555449.5, -656695, -964734,-8876, -200016, -630544, -37042, -1021108, -434836, -113367, -650265, -765307.5,-358117, -254566, -579852, -462318, -810289, -49044, -650422, -555449.5, -660188], "given", "selpers", 8, fileprefix,delete_logs=False, allow_unknowns=10, ))
print(curr_time())
sys.stdout=o