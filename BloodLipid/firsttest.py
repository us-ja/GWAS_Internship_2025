import sys
sys.path.append('..')
import random
from my_utils import *
fileprefix="blood_lipid_cleaned"



for seed in range(200, 210):
    grouping25(fileprefix, 300, seed)
    