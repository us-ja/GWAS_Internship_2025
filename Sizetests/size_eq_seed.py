import sys
sys.path.append('..')
from my_utils import *
fileprefix="HapMap"
hap=open("HapMap.ped")
l=hap.readlines()

for seed in range(225, 825, 25):
    pyramid25(fileprefix, seed, seed, plines=l, )