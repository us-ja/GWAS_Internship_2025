import sys
sys.path.append('..')
import random
from my_utils import *

predic_acc=conversion(6, "total", "total", 0, "testdata_2", delete_logs=False)     #does not work
print(predic_acc)
predic_acc=conversion(list(range(20)), "given", "total", 0, "testdata_2", delete_logs=False)#works
print(predic_acc)

   