
import sys 
sys.path.append('..')
from my_utils import *
o = sys.stdout   #define std as o


fileprefix="HapMap"


total_snp=get_total_snp(fileprefix)# total_snp=170 #for tests only


print(curr_time())
print(conversion([-833028, -561835, -763207, -820289, -555449.5, -167750, -137839.5], "given", "l_3entire", 8, fileprefix,delete_logs=False, allow_unknowns=10, sel_pers=list(range(100))))
print(curr_time())
sys.stdout=o